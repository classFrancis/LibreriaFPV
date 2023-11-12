-- ESTOS SON AUTORES Y LIBROS PARA INGRESAR DIRECTAMENTE EN LA BASE DE DATOS SOLO PARA PRUEBAS --
-- POR SI ES NECESARIO ACTUALIZAR EL MODELO --

INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Gabriel', 'García Márquez', 'Biografía del autor...');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('Cien años de soledad', "imagenes_libros/cien_soledad.png", 1, 'Novela', 'Editorial Hispanoamericana', '1ra', '1967-06-05', 100, 19.99, TRUE);

INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Julio', 'Cortázar', 'Biografía de Julio Cortázar, escritor argentino...');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('Rayuela', "imagenes_libros/rayuela.png", 2, 'Novela', 'Editorial Pantheon', '1ra', '1963-06-01', 50, 15.99, TRUE);

INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Isabel', 'Allende', 'Isabel Allende es una escritora chilena de fama mundial, conocida por sus novelas que combinan el realismo mágico con la narración política y personal.');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('La casa de los espíritus', "imagenes_libros/casa_espiritus.png", 3, 'Realismo mágico', 'Editorial Sudamericana', '1ra', '1982-01-01', 80, 22.50, TRUE);

INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Mario', 'Vargas Llosa', 'Mario Vargas Llosa es un escritor y político peruano, uno de los más importantes novelistas y ensayistas contemporáneos.');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('La fiesta del chivo', "imagenes_libros/fiesta_chivo.png", 4, 'Histórica', 'Alfaguara', '1ra', '2000-01-01', 50, 19.95, TRUE);

INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Jorge Luis', 'Borges', 'Escritor argentino, uno de los literatos más destacados del siglo XX...');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('Ficciones', "imagenes_libros/ficcion.png", 5, 'Cuentos', 'Editorial Sur', '1ra', '1944-01-01', 60, 18.00, TRUE);

INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Haruki', 'Murakami', 'Autor japonés conocido por su narrativa surrealista y su capacidad para mezclar lo cotidiano con lo fantástico...');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('Kafka en la orilla', "imagenes_libros/kafka.png", 6, 'Realismo mágico', 'Tusquets Editores', '1ra', '2002-01-01', 70, 20.99, TRUE);

INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Virginia', 'Woolf', 'Escritora británica, figura destacada del modernismo literario del siglo XX...');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('Mrs Dalloway', "imagenes_libros/mrs_dalloway.png", 7, 'Novela', 'Hogarth Press', '1ra', '1925-05-14', 50, 15.00, TRUE);

INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Leo', 'Tolstoy', 'Escritor ruso, uno de los novelistas más famosos y reconocidos de la literatura mundial...');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('Guerra y Paz', "imagenes_libros/guerra.png", 8, 'Novela histórica', 'Editorial Rusa Clásica', '1ra', '1869-01-01', 40, 24.99, TRUE);

INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Franz', 'Kafka', 'Escritor de origen judío nacido en Bohemia, es una de las figuras literarias más influyentes del siglo XX...');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('La Metamorfosis', "imagenes_libros/metamorfosis.png", 9, 'Novela corta', 'Editorial Praga', '1ra', '1915-01-01', 80, 12.99, TRUE);

INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Louisa May', 'Alcott', 'Escritora estadounidense, conocida principalmente por su novela "Mujercitas"...');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('Mujercitas', "imagenes_libros/girls.png", 10, 'Novela', 'Editorial Americana', '1ra', '1868-01-01', 70, 14.50, TRUE);