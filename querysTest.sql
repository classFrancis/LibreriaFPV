-- ESTOS SON AUTORES Y LIBROS PARA INGRESAR DIRECTAMENTE EN LA BASE DE DATOS SOLO PARA PRUEBAS --
-- POR SI ES NECESARIO ACTUALIZAR EL MODELO --


INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Gabriel', 'García Márquez', 'Biografía del autor...');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('Cien años de soledad', NULL, 1, 'Novela', 'Editorial Hispanoamericana', '1ra', '1967-06-05', 100, 19.99, TRUE);

INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Julio', 'Cortázar', 'Biografía de Julio Cortázar, escritor argentino...');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('Rayuela', NULL, 2, 'Novela', 'Editorial Pantheon', '1ra', '1963-06-01', 50, 15.99, TRUE);

INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Isabel', 'Allende', 'Isabel Allende es una escritora chilena de fama mundial, conocida por sus novelas que combinan el realismo mágico con la narración política y personal.');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('La casa de los espíritus', NULL, 3, 'Realismo mágico', 'Editorial Sudamericana', '1ra', '1982-01-01', 80, 22.50, TRUE);


INSERT INTO libreriaapp_autor (nombreAutor, apellidoAutor, biografiaAutor)
VALUES ('Mario', 'Vargas Llosa', 'Mario Vargas Llosa es un escritor y político peruano, uno de los más importantes novelistas y ensayistas contemporáneos.');

INSERT INTO libreriaapp_libro (titulo, imagen, autorlibro_id, tematica, editorial, edicion, fechaDePublicacion, cantidad, precio, disponible)
VALUES ('La fiesta del chivo', NULL, 4, 'Histórica', 'Alfaguara', '1ra', '2000-01-01', 50, 19.95, TRUE);