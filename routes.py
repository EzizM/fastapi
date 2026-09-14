from fastapi import APIRouter, Request, Response
from pydantic import BaseModel, Field
from typing import List
from db.crud import (
    get_all_products,
    create_product,
    get_product_by_id,
    get_product_by_title,
    create_order,
    get_all_order,
    get_order_by_id
)

router = APIRouter()


class ProductModel(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    desc: str = Field(..., min_length=5)
    price: float = Field(..., gt=0)
    image_url: str

class OrderItemModel(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)

class OrderCreateModel(BaseModel):
    user_id: int
    items: List[OrderItemModel]

@router.post('/product/add')
async def product_add(data: ProductModel):
    return await create_product(data.title, data.desc, data.price, data.image_url)


@router.get('/products')
async def get_products(order_by: str = 'id', direction: str = 'asc'):
    return await get_all_products(order_by, direction)

@router.get('/product/{product_id}')
async def get_product(product_id: int):
    return await get_product_by_id(product_id)

@router.get('/product/search/{title}')
async def get_product_title(title: str):
    return await get_product_by_title(title)

@router.get('/orders')
async def get_orders():
    return await get_all_order()

@router.get('/orders/{order_id}')
async def get_product(order_id: int):
    return await get_order_by_id(order_id)

@router.post('/order/add')
async def order_add(data: OrderCreateModel):
    return await create_order(data.user_id, [item.model_dump() for item in data.items])

@router.post("/webhook/fondy")
async def fondy_callback(request: Request):
    content_type = request.headers.get('content-type', '')

    if 'application/json'in content_type:
        data = await request.json()
    elif 'application/x-www-form-urlencoded' in content_type:
        form_data = await request.form()
        data = dict(form_data)
    else:
        return Response(status_code=400, content='Unsupported content type')





# from db.models import Product
# from db.connect import async_session
# async def seed_products():
#     fake_data = [
#         ("Belt", "Black belt", 10.99, "https://n.nordstrommedia.com/it/14edd79a-299a-495c-8d34-47d31a6cabd4.jpeg?w=780&h=1170&crop=pad&dpr=2"),
#         ("T-Shirt", "Cotton t-shirt", 20.99, "https://images.asos-media.com/products/fred-perry-twin-tipped-t-shirt-in-black/211312677-1-black?$n_750w$&wid=750&fit=constrain"),
#         ("Jeans", "Denim jeans", 30.99, "https://mnml.la/cdn/shop/files/Mule-Pocket-Kick-Flare-Denim-Rinsed-Indigo-2.jpg?format=pjpg&v=1780391613&width=1622"),
#         ("Shoes", "Running shoes", 40.99, "https://static.nike.com/a/images/t_web_pdp_535_v2/f_auto,u_9ddf04c7-2a9a-4d76-add1-d15af8f0263d,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/a6c7f607-00e5-4395-9774-4c67410a19c7/W+NIKE+ACG+ZEGAMA+TRAIL.png"),
#         ("Hat", "Baseball hat", 50.99, "https://fanatics.frgimages.com/new-york-yankees/mens-new-era-navy-new-york-yankees-game-authentic-collection-on-field-59fifty-fitted-hat_pi2659000_altimages_ff_2659252alt1_full.jpg?_hv=2&w=1018"),
#     ]
#     async with async_session() as session:
#         for title, desc, price, image_url in fake_data:
#             session.add(Product(title=title, desc=desc, price=price, image_url=image_url))
#         await session.commit()



# @router.put('/users/{user_id}')
# async def update_user_data(user_id: int, data: UserModel):
#     return await update_user(user_id, data.name, data.email)

# @router.delete('/users/{user_id}')
# async def delete_user_data(user_id: int):
#     return await delete_user(user_id)

