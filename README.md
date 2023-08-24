# DBP-Anime

Desarrollado por Gabriel Eduardo Romero Diez

### Descripción general:
Esta es una API que utiliza Flask, Flask-RESTful, Flask-JWT-Extended y SQLAlchemy para proporcionar una solución de backend para una aplicación de anime con usuarios y categorías. La aplicación es capaz de:

- Registrar y autenticar usuarios.
- Proteger rutas con JWT.
- Crear, leer, actualizar y eliminar animes y categorías.

### Componentes clave:

1. **Configuración**: 
   - La clave secreta JWT se establece usando `JWT_SECRET_KEY`.
   - La conexión a la base de datos se configura con `SQLALCHEMY_DATABASE_URI` y apunta a una base de datos PostgreSQL.
   
2. **Modelos**:
   - `UserModel`: Representa a un usuario con un nombre de usuario y una contraseña cifrada.
   - `CategoryModel`: Representa categorías para animes, como "Acción" o "Romance".
   - `AnimeModel`: Representa información sobre un anime, incluidas las categorías a las que pertenece.

3. **Recursos y rutas**:
   - `Login`: POST a `/login` para autenticarse. Devuelve un token JWT si es exitoso.
   - `Register`: POST a `/register` para registrar un nuevo usuario.
   - `User`: GET a `/user` devuelve la información del usuario autenticado.
   - `Category`: GET, POST, DELETE a `/category/<int:category_id>` para recuperar, crear o eliminar una categoría.
   - `CategoryList`: GET a `/categories` para obtener una lista de todas las categorías.
   - `Anime`: GET, POST, DELETE, PUT, PATCH a `/anime/<int:anime_id>` para realizar operaciones CRUD en animes.
   - `AnimeList`: GET a `/animes` para obtener una lista de todos los animes.

### Pasos iniciales para poner en marcha la API:

1. **Instalación de paquetes**:
   Antes de ejecutar la API, asegúrate de tener todos los paquetes necesarios instalados. Puedes hacerlo con pip:
   ```bash
   pip install Flask Flask-RESTful Flask-JWT-Extended Flask-SQLAlchemy psycopg2-binary
   ```

2. **Base de datos**:
   - La API está configurada para conectarse a una base de datos PostgreSQL con el nombre "anime" en el localhost, usando el usuario "gabo" y la contraseña "papa1234".
   - Antes de ejecutar la aplicación, asegúrate de que la base de datos exista y esté accesible con las credenciales proporcionadas.

3. **Ejecución**:
   - Si todo está configurado correctamente, simplemente ejecuta el script en tu terminal para iniciar el servidor:
   ```bash
   python your_script_name.py
   ```

   Esto iniciará un servidor Flask en el puerto 5000. Puedes acceder a la API en `http://localhost:5000`.

4. **Rutas protegidas**:
   - Muchas de las rutas en esta API requieren autenticación. Esto significa que tendrás que enviar un token JWT en el encabezado de la solicitud para acceder a estas rutas. Puedes obtener un token JWT haciendo una solicitud POST exitosa a `/login` con un nombre de usuario y contraseña válidos.

