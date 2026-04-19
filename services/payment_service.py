import mercadopago
from flask import current_app, url_for

#CREAR PREFERENCIA DE MERCADO PAGO
#CONSULTAR DOCUMENTACION 
def crear_preferencia(pedido):

    token = current_app.config.get("MP_ACCESS_TOKEN")

    base_url = current_app.config.get("BASE_URL")

    if not token:
        raise ValueError("MP_ACCESS_TOKEN no configurado")
    
    sdk=mercadopago.SDK(token)

    items_mp=[]

    for item in pedido.items:
        items_mp.append({
            "title": item.producto.nombre,
            "quantity":item.cantidad,
            "unit_price": float(item.precio_unitario)
        })
    preference_data={
        "items":items_mp,
        "back_urls":{
            "success": f'{base_url}/checkout/success',
            "failure": f'{base_url}/checkout/failure',
            "pending": f'{base_url}/checkout/pending'
        },
        "auto_return": "approved",
        "notification_url": f'{base_url}/checkout/webhook',
        "external_reference": str(pedido.id_pedido)
    }

    preference_response=sdk.preference().create(preference_data)

    print (preference_response)

    if preference_response["status"] != 201:
        raise Exception("Error al crear preferencia en MercadoPago")

    return preference_response["response"]['init_point']