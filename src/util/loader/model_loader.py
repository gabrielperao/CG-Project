class ModelLoader:

    @staticmethod
    def load_from_file(filename: str) -> dict:
        """Loads a Wavefront OBJ file. """
        objects = {}
        vertices = []
        texture_coords = []
        faces = []

        material = None

        for line in open(filename, "r"):  # para cada linha do arquivo .obj
            if line.startswith('#'):
                continue  # ignora comentarios
            values = line.split()  # quebra a linha por espaço
            if not values:
                continue

            if values[0] == 'v':  # recuperando vertices
                vertices.append(values[1:4])
            elif values[0] == 'vt':  # recuperando coordenadas de textura
                texture_coords.append(values[1:3])
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'f':  # recuperando faces
                face = []
                face_texture = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)

                faces.append((face, face_texture, material))

        model = {'vertices': vertices, 'texture': texture_coords, 'faces': faces}
        return model
