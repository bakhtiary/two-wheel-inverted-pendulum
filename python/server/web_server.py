from construct.lib import Container
from aiohttp import web

from server.data_descriptors import DataDescriptorsFactory, DataDescriptors


def get_input_forms(control_data):
    fields = ""
    for name in control_data:
        val = control_data[name]
        fields += f"""
            <label for="{name}">{name}</label>
            <input id="{name}" name="{name}" type="text" value="{val}" autofocus/>
        """

    return fields


def get_data_list_markup(control_data_list):
    forms = ""
    for id in control_data_list:
        _, control_data, form_name, _ = control_data_list[id]
        forms += f""" {form_name} :
        <form action="/set_values" method="post" accept-charset="utf-8"
              enctype="application/x-www-form-urlencoded">
        
        {get_input_forms(control_data)}
        
            <input type="submit" value="upload new values"/>
        </form>
        """

    return forms


def get_form(control_data_list):
    return f"""
    <html>
    <head>
    </head>
    <body>
    {get_data_list_markup(control_data_list)}   
    
    </body>
    </html>
    """


def run_ui_web_server(q, data_descriptors_factory: DataDescriptorsFactory):

    class WebServer:
        def __init__(self, data_descriptors_factory: DataDescriptorsFactory):
            self.data_descriptors: DataDescriptors = data_descriptors_factory.makeDD()

        async def handle(self, request):
            form = get_form(self.data_descriptors.id_maps_to_structs_container_name_tupple)
            return web.Response(body=form, content_type='text/html')

        async def set_value(self, request):
            data = await request.post()
            data_dict = {}
            form_id = int(data['id'])
            the_data_format = self.data_descriptors.id_maps_to_structs_container_name_tupple[form_id]
            control_data = the_data_format[1]
            data_type_converters = the_data_format[3]
            for name in control_data:
                data_dict[name] = data_type_converters[name](data[name])
            data_in_container = Container(data_dict)
            q.put(data_in_container)

            return web.Response(body=get_form(self.data_descriptors.id_maps_to_structs_container_name_tupple), content_type='text/html')

    server = WebServer(data_descriptors_factory)

    app = web.Application()
    app.add_routes([web.get('/', server.handle),
                    web.post('/set_values', server.set_value)])

    web.run_app(app, port=8080)