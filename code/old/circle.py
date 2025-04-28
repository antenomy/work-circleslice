import numpy as np

class Circle():
    def __init__(self, radius, center = (0, 0)):
        self.radius = radius
        self.position = center
        
        # theta = np.linspace(0, 2 * np.pi, 360, endpoint=False)
        # x = center[0] + radius * np.cos(theta)
        # y = center[1] + radius * np.sin(theta)
        # return np.column_stack((x, y))
    
    def get_y_from_x(self, x_position):
        # Extract the center of the circle
        h, k = self.position
        r = self.radius
        
        # Check if x_position is within the valid range
        if abs(x_position - h) > r:
            raise ValueError("x_position is out of the circle's range")
        
        # Calculate the corresponding y values using the circle equation
        y_positive = k + np.sqrt(r**2 - (x_position - h)**2)  # Upper half of the circle
        y_negative = k - np.sqrt(r**2 - (x_position - h)**2)  # Lower half of the circle
        
        return y_positive, y_negative
    
    def get_line_intersections(self, line_k = None, line_m = 0, vertical_x = None):
        
        h, k = self.position
        if vertical_x is not None:
            
            discriminant = self.radius**2 - (vertical_x - h)**2
            if discriminant >= 0:
                # Calculate the corresponding y values using the circle equation
                y_positive = k + np.sqrt(discriminant)  # Upper half of the circle
                y_negative = k - np.sqrt(discriminant)  # Lower half of the circle
                return [(vertical_x, y_positive), (vertical_x, y_negative)]
            else:
                return []
            
        elif line_k is not None:
            # Comes from a rewriting of the expression (x-self.position[0])^2 + (line_kx + line_m - self.position[1])^2 = self.radius
            A = 1 + line_k**2
            B = -2*h + 2*line_k*(line_m - k)
            C = h**2 + (line_m - k)**2 - self.radius**2
            
            x_roots = np.roots([A,B,C])
            real_roots = [float(root.real) for root in x_roots if np.isclose(root.imag, 0)]
            return [(x_root, (line_k*x_root + line_m)) for x_root in real_roots]