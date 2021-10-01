from construct.lib import Container
from aiohttp import web


def get_input_list(control_data):
    fields = ""
    for name in control_data:
        val = control_data[name]
        fields += f"""
            <label for="{name}">{name}</label>
            <input id="{name}" name="{name}" type="text" value="{val}" autofocus/>
        """

    return fields


def get_form(control_data):
    return f"""
    <html>
    <head>
    </head>
    <body>
    <form action="/set_values" method="post" accept-charset="utf-8"
          enctype="application/x-www-form-urlencoded">
    
    {get_input_list(control_data)}
    
        <input type="submit" value="upload new values"/>
    </form>
    </body>
    </html>
    """


def run_ui_web_server(q, control_data):

    async def handle(request):
        return web.Response(body=get_form(control_data),content_type='text/html')

    async def set_value(request):
        data = await request.post()
        data_dict = {}
        for name in control_data:
            data_dict[name] = float(data[name])
        data_in_container = Container(data_dict)
        print(data_in_container)
        q.put(data_in_container)

        return web.Response(body=get_form(data_in_container),content_type='text/html')

    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.post('/set_values', set_value)])

    web.run_app(app, port=8080)