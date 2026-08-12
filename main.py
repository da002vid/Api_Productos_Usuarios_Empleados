from fastapi import FastAPI, HTTPException
from database import crear_tabla, crear_tabla_usuarios, crear_tabla_empleados, crear_tabla_categorias, crear_tabla_productos, get_connection
from models import Product, User, Employee, Category, Item

app = FastAPI()

crear_tabla()
crear_tabla_usuarios()
crear_tabla_empleados()
crear_tabla_categorias()
crear_tabla_productos()


@app.get("/")
def home():
    return {"Mensaje": "Api Funcionando Correctamente"}


@app.post("/products")
def create_product(product: Product):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO " \
    "products(code,name,price,stock) VALUES(%s,%s,%s,%s)" \
    "RETURNING code",
    (product.code, product.name, product.price, product.stock))
    new_code = cur.fetchone()["code"]
    conn.commit()
    cur.close()
    conn.close()
    return {"Mensaje":"Producto Creado", "code":new_code}


@app.get("/products")
def list_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return {"productos": products}


@app.get("/products/{code}")
def buscar_producto(code: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT code, name, price, stock FROM products WHERE code = %s", (code,))
    product = cur.fetchone()
    cur.close()
    conn.close()

    if product:
        return product
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.put("/products/{code}")
def update_product(code: int, product: Product):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE products SET name = %s, price = %s, stock = %s WHERE code = %s", (product.name, product.price, product.stock, code))
    affect_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if affect_rows == 0:
        raise HTTPException(status_code=404,detail="Producto No Encontrado") 
    return{"msg": "Producto actualizado exitosamente"}


@app.delete("/products/{code}")
def delete_product(code: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE code = %s", (code,))
    affect_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if affect_rows == 0:
        raise HTTPException(status_code=404, detail="Producto No Encontrado")
    return {"msg": "Producto eliminado exitosamente"}


@app.post("/usuarios")
def create_user(user: User):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(username,password) VALUES(%s,%s)",
    (user.username, user.password))
    conn.commit()
    cur.close()
    conn.close()
    return {"Mensaje": "Usuario Creado"}


@app.post("/login")
def verificar_usuario(user: User):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s",
    (user.username, user.password))
    resultado = cur.fetchone()
    cur.close()
    conn.close()

    if resultado:
        return {"Mensaje": "existe"}
    return {"Mensaje": "no existe"}


@app.post("/empleados")
def create_employee(employee: Employee):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO " \
    "employees(document,name,position,salary) VALUES(%s,%s,%s,%s)" \
    "RETURNING document",
    (employee.document, employee.name, employee.position, employee.salary))
    new_document = cur.fetchone()["document"]
    conn.commit()
    cur.close()
    conn.close()
    return {"Mensaje":"Empleado Creado", "document":new_document}


@app.get("/empleados")
def list_employees():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    cur.close()
    conn.close()
    return {"empleados": employees}


@app.get("/empleados/{document}")
def buscar_empleado(document: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT document, name, position, salary FROM employees WHERE document = %s", (document,))
    employee = cur.fetchone()
    cur.close()
    conn.close()

    if employee:
        return employee
    raise HTTPException(status_code=404, detail="Empleado no encontrado")


@app.put("/empleados/{document}")
def update_employee(document: int, employee: Employee):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE employees SET name = %s, position = %s, salary = %s WHERE document = %s", (employee.name, employee.position, employee.salary, document))
    affect_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if affect_rows == 0:
        raise HTTPException(status_code=404,detail="Empleado No Encontrado") 
    return{"msg": "Empleado actualizado exitosamente"}


@app.delete("/empleados/{document}")
def delete_employee(document: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE document = %s", (document,))
    affect_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if affect_rows == 0:
        raise HTTPException(status_code=404, detail="Empleado No Encontrado")
    return {"msg": "Empleado eliminado exitosamente"}


@app.post("/categorias")
def crear_categoria(categoria: Category):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM categorias WHERE nombre = %s", (categoria.name,))
    existe = cur.fetchone()
    if existe:
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="La categoria ya existe")

    cur.execute("INSERT INTO categorias(nombre) VALUES(%s) RETURNING id", (categoria.name,))
    nuevo_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return {"Mensaje": "Categoria Creada", "id": nuevo_id}


@app.get("/categorias")
def listar_categorias():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM categorias")
    categorias = cur.fetchall()
    cur.close()
    conn.close()
    return {"categorias": categorias}


@app.get("/categorias/{id}/productos")
def listar_productos_por_categoria(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos WHERE categoria_id = %s", (id,))
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return {"productos": productos}


@app.get("/categorias/{id}")
def buscar_categoria(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM categorias WHERE id = %s", (id,))
    categoria = cur.fetchone()
    cur.close()
    conn.close()

    if categoria:
        return categoria
    raise HTTPException(status_code=404, detail="Categoria no encontrada")


@app.delete("/categorias/{id}")
def eliminar_categoria(id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM categorias WHERE id = %s", (id,))
        affect_rows = cur.rowcount
        conn.commit()
    except:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="No se puede eliminar, la categoria tiene productos asociados")

    cur.close()
    conn.close()
    if affect_rows == 0:
        raise HTTPException(status_code=404, detail="Categoria No Encontrada")
    return {"msg": "Categoria eliminada exitosamente"}


@app.post("/productos")
def crear_producto(producto: Item):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM categorias WHERE id = %s", (producto.category_id,))
    categoria = cur.fetchone()
    if not categoria:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="La categoria indicada no existe")

    cur.execute("INSERT INTO " \
    "productos(nombre,precio,stock,categoria_id) VALUES(%s,%s,%s,%s)" \
    "RETURNING id",
    (producto.name, producto.price, producto.stock, producto.category_id))
    nuevo_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return {"Mensaje": "Producto Creado", "id": nuevo_id}


@app.get("/productos")
def listar_productos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return {"productos": productos}


@app.get("/productos/stock-bajo/{minimo}")
def productos_stock_bajo(minimo: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos WHERE stock < %s", (minimo,))
    productos = cur.fetchall()       
    cur.close()
    conn.close()
    return {"productos": productos}


@app.get("/productos/{id}")
def buscar_producto_id(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cur.fetchone()
    cur.close()
    conn.close()

    if producto:
        return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.put("/productos/{id}")
def actualizar_producto(id: int, producto: Item):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM categorias WHERE id = %s", (producto.category_id,))
    categoria = cur.fetchone()
    if not categoria:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="La categoria indicada no existe")

    cur.execute("UPDATE productos SET nombre = %s, precio = %s, stock = %s, categoria_id = %s WHERE id = %s",
    (producto.name, producto.price, producto.stock, producto.category_id, id))
    affect_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if affect_rows == 0:
        raise HTTPException(status_code=404, detail="Producto No Encontrado")
    return {"msg": "Producto actualizado exitosamente"}


@app.delete("/productos/{id}")
def eliminar_producto(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM productos WHERE id = %s", (id,))
    affect_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if affect_rows == 0:
        raise HTTPException(status_code=404, detail="Producto No Encontrado")
    return {"msg": "Producto eliminado exitosamente"}