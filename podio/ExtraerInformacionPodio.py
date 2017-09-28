from bs4 import BeautifulSoup


class ExtraerInformacionPodio():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def getFieldValue(self, field, _client, no_html=False, external_id=True, depth=1):
        """
        Gets the value of a field from its raw JSON data

        Params:
            depth: If there is a relationship field and depth has a value greater than zero, it will fetch that item's dictionary data from the PODIO api and use it as the value. If false, it will use the item_id value
            no_html: Defines whether HTML will be stripped or not
        """

        if field["type"] == "category":
            if field["config"]["settings"]["multiple"]:
                values = []
                for category in field["values"]:
                    values.append(category["value"]["text"])
                return values
            else:
                return field["values"][0]["value"]["text"]
        elif field["type"] == "image":
            values = []
            for image in field['values']:
                values.append([image["value"]["mimetype"], image["value"]["file_id"]])
            return values
        elif field["type"] == "date":
            return field["values"][0]
        elif field["type"] == "app":
            itemID = field["values"][0]["value"]["item_id"]
            if depth <= 0:
                return itemID
            else:
                data = _client.Item.find(int(itemID))
                if not external_id:
                    item = self.make_dict(data, external_id=external_id, depth=depth - 1)
                else:
                    item = self.makeDict(data, nested=_client)
                return item
        elif field["type"] == "text":
            text = field["values"][0]["value"]
            if no_html and field["config"]["settings"]["format"] == 'html':
                print(text.encode('utf-8'))
                html_text = BeautifulSoup(text, "html5lib")
                for p_tag in html_text.find_all('p'):
                    p_tag.unwrap()

                for br_tag in html_text.find_all('br'):
                    br_tag.name = "text:line-break"
                html_text.find('html').unwrap()
                html_text.find('head').unwrap()
                html_text.find('body').unwrap()
                text = (html_text)
                print(text.encode('ascii', 'ignore'))
                # text = strip_tags(text)
            return text
        elif field["type"] == "embed":
            return field["values"][0]["embed"]["url"]
        else:
            # print field["type"]
            return field["values"][0]["value"]

    def makeDict(self, item, nested=False, no_html=False):
        """
        Creates a dictionary with the external_id of the item's fields ad keys, and their values as the dictionary values.
        """
        dictionary = dict(
            [(field["external_id"], self.getFieldValue(field, nested, no_html)) for field in item["fields"]])
        return {'item': item["item_id"], 'values': dictionary, 'initial_revision': item["initial_revision"]}

    def make_dict(self, item, external_id=True, no_html=False, depth=1, version='v1'):
        """
        Creates a dictionary with the external_id of the item's fields ad keys, and their values as the dictionary values. This second versions allows to choose between the field_id or the external_id for the dictionary's key, and adds the field type to the generated dictionary.
        Params:
            item: The item that is being retrieved
            depth: the number of levels that related apps will be followed
        """
        if external_id:
            key_type = "external_id"
        else:
            key_type = "field_id"

        dictionary = dict([(field[key_type], {"type": field["type"],
                                              "value": self.getFieldValue(field, no_html, external_id=external_id,
                                                                          depth=depth)}) for field in item["fields"]])
        return {'item': item["item_id"], 'values': dictionary}