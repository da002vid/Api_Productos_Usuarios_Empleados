from fastapi import FastAPI, HTTPException
from database import crear_tabla, crear_tabla_usuarios, crear_tabla_empleados, get_connection
from models import Product, User, Employee

app = FastAPI()

crear_tabla()
crear_tabla_usuarios()
crear_tabla_empleados()


@app.get("/")
def home():
    return {"Mensaje": "Api Funcionando Correctamente"}


@app.post("/productos")
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


@app.get("/productos")
def list_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return {"productos": products}


@app.get("/productos/{code}")
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


#ACTUALIZAR UN REGISTRO
@app.put("/productos/{code}")
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


@app.delete("/productos/{code}")
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


#REGISTRAR UN USUARIO
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


#CONSULTAR SI EXISTE UN USUARIO Y PASSWORD
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


#REGISTRAR UN EMPLEADO
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


#ACTUALIZAR UN REGISTRO
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