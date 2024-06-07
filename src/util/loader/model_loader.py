class ModelLoader:

    @staticmethod
    def load_from_file(filename: str) -> dict:
        """Loads a Wavefront OBJ file. """
        vertexes = []
        normals = []
        texture_coord = []
        faces = []
        material = None

        # itera sobre as linhas do arquivo .obj
        for line in open(filename, "r"):
            # ignora as linhas de comentários
            if line.startswith('#'):
                continue
            # separa os valores da linha pelo espaço
            values = line.split()
            if not values:
                continue

            if values[0] == 'v':  # coordenadas dos vértices
                vertexes.append(values[1:4])
            elif values[0] == 'vt':  # coordenadas de textura
                texture_coord.append(values[1:3])
            elif values[0] == 'vn':  # coordenadas das normais
                normals.append(values[1:4])
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'f':  # mapeamento das faces
                face = []
                face_texture = []
                face_normals = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    face_normals.append(int(w[2]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)

                faces.append((face, face_texture, face_normals, material))

        return {'vertices': vertexes, 'texture': texture_coord, 'normals': normals, 'faces': faces}
