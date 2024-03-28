    def build_matrix_cell(self):
        """
        Generates coordinates and topology for a matrix object based on a single cell. 
        
        Parameters:
            self.tissue.cell_gro_content (dict): The individual cell coordinates
            
        Returns:
            self.matrix_coords (dict): Atom names and coords of matrix element (dict key = atom index). 
                This dict is required for constructing the topology. 
            self.system_coords (dict): Combined  dict of cell + matrix. 
                This dict is required for parsing the final system coordinates. 

        Todo:
             - Allow different matrix bead names than MX1
             - Multiple layers stack oddly
        """
        json_values = self.json_parser.json_values
        matrix_layers = json_values["nr_of_layers"]
        #matrix_beads = json_values["matrix_beads"] - currently unused!
        
        matrix_z_offset = 0.4 # in nm, distance between cell and first matrix layer

        # we fit the matrix under the cell in z-direction, thus need to look for 'lowest'
        # z coordinate in the system (in this case, a single cell)
        lowest_z = min(atom['coords'][2] for atom in self.tissue.cell_gro_content.values())
        
        #want to center the matrix with respect to the cell on top
        center_x = sum(atom['coords'][0] for atom in self.tissue.cell_gro_content.values()) / len(self.tissue.cell_gro_content)
        center_y = sum(atom['coords'][1] for atom in self.tissue.cell_gro_content.values()) / len(self.tissue.cell_gro_content)

        #we can know the x,y length of the matrix plane too from the coordinates
        # and then multiply them by a matrix length factor afterwards, to have a larger matrix.
        max_x = max(atom['coords'][0] for atom in self.tissue.cell_gro_content.values())
        max_y = max(atom['coords'][1] for atom in self.tissue.cell_gro_content.values())
        matrix_x = max_x * 2
        matrix_y = max_y * 2
        
        atom_index = 0

        for layer in range(matrix_layers):
            z_offset = lowest_z - matrix_z_offset - (layer+1) * matrix_z_offset
            # Generate matrix particles centered at (0, 0, 0) with adjusted z coordinate
            for x in range(int(matrix_x) + 1):
                for y in range(int(matrix_y) + 1):
                    particle = {
                        'name': 'MX1',
                        'coords': [x - matrix_x / 2 + center_x, y - matrix_y / 2 + center_y, z_offset],
                    }
                    self.matrix_coords[atom_index] = particle
                    atom_index += 1
                
        #after preparing the matrix coordinates, we finalize the self.system_coords dict
        # continue from last index of CELL
        last_index = max(self.tissue.cell_gro_content.keys())
        self.system_coords = self.tissue.cell_gro_content.copy()

        next_index = last_index + 1
        # then add the matrix dict but index the atom indices again!
        for atom_index, atom_info in self.matrix_coords.items():
            new_atom_info = {
                'name': atom_info['name'],
                'coords': atom_info['coords']
            }
            self.system_coords[next_index] = new_atom_info
            next_index += 1
        
        self.build_matrix_top()
        
    def build_matrix_tissue(self):
        """
        Generates coordinates and topology for a matrix object based on a tissue.  
        
        Parameters:
            self.tissue.tissue_coords (dict): The individual cell coordinates
            
        Returns:
            self.matrix_coords (dict): Atom names and coords of matrix element (dict key = atom index)
                This dict is required for constructing the topology. 
            self.system_coords (dict): Combined  dict of tissue + matrix. 
                This dict is required for parsing the final system coordinates. 

        Todo:
             - Allow different matrix bead names than MX1
             - Multiple layers stack oddly
        """
        json_values = self.json_parser.json_values
        matrix_layers = json_values["nr_of_layers"] #only 1 currently works well.
        #matrix_beads = json_values["matrix_beads"] - currently unused!
        
        matrix_z_offset = 0.4 # in nm, distance between cell and first matrix layer

        # logic is exactly the same as for single CELL, so removed comments
        lowest_z = min(atom['coords'][2] for atom in self.tissue.tissue_coords.values())
        center_x = sum(atom['coords'][0] for atom in self.tissue.tissue_coords.values()) / len(self.tissue.tissue_coords)
        center_y = sum(atom['coords'][1] for atom in self.tissue.tissue_coords.values()) / len(self.tissue.tissue_coords)

        max_x = max(atom['coords'][0] for atom in self.tissue.tissue_coords.values())
        max_y = max(atom['coords'][1] for atom in self.tissue.tissue_coords.values())
        matrix_x = max_x * 4
        matrix_y = max_y * 4

        atom_index = 0

        for layer in range(matrix_layers):
            z_offset = lowest_z - matrix_z_offset - (layer + 1) * matrix_z_offset
            # Generate matrix particles centered at (0, 0, 0) with adjusted z coordinate
            for x in range(int(matrix_x) + 1):
                for y in range(int(matrix_y) + 1):
                    particle = {
                        'name': 'MX1',
                        'coords': [x - matrix_x / 2 + center_x, y - matrix_y / 2 + center_y, z_offset],
                    }
                    self.matrix_coords[atom_index] = particle
                    atom_index += 1
        
        #after preparing the matrix coordinates, we finalize the self.system_coords dict
        # continue from last index of CELL
        last_index = max(self.tissue.tissue_coords.keys())
        self.system_coords = self.tissue.tissue_coords.copy()
        
        next_index = last_index + 1
        # then add the matrix dict but index the atom indices again!
        for atom_index, atom_info in self.matrix_coords.items():
            new_atom_info = {
                'name': atom_info['name'],
                'coords': atom_info['coords']
            }
            self.system_coords[next_index] = new_atom_info
            next_index += 1
        
        self.build_matrix_top()