import math

pipe_types = {
    'Riveted steel': 4.95,
    'Concrete': 1.65,
    'Wood stave': 0.54,
    'Cast iron': 0.26,
    'Galvanized iron': 0.15,
    'Commerical steel - Wrought iron': 0.045,
    'Drawn tubing': 0.0015,
    'Plastic - Glass': 0,
}
pipe_diameters = [0.015, 0.020, 0.025, 0.040, 0.050, 0.080, 0.100, 0.125,0.150,0.200,0.250,0.300] # in meter
electric_cost = 0.04 # dolar/KW
flow_rate = 0.0139 # m^3/s
KL_minor_total = 9.05
pump_efficiency = 70/100
Lenght = 10000 # meter
viscosity = 2.9825*10**-4 # Ns/m^2
density = 961.85 #Kg/m^3
gravitational_acceleration = 9.81 # m/s^2
elevation_difference_h2 = 20 # meter

def area_calculator(the_diameter):
    area = (math.pi*(the_diameter**2))/4
    return area
def velocity_calculator(the_diameter):
    area = area_calculator(the_diameter)
    velocity = flow_rate/area
    return velocity
def reynolds_number_calculator(the_diameter):
    velocity = velocity_calculator(the_diameter)
    reynolds_number = (density*velocity*the_diameter)/viscosity
    return reynolds_number
def minor_calculator(the_diameter):
    velocity = velocity_calculator(the_diameter)
    minor = KL_minor_total*(velocity**2)/2
    return minor
def f_calculator(the_diameter,coefficent):
    Re_number = reynolds_number_calculator(the_diameter)
    f = (1 / (-1.8 * math.log10((coefficent / the_diameter) / 3.7 + (6.9 / Re_number)))) ** 2
    return f
def major_calculator(f,the_diameter):
    velocity = velocity_calculator(the_diameter)
    major = f*(Lenght/the_diameter)*(velocity**2)/2
    return major
def pump_power_calculator(the_pipe_coefficient , the_diameter):
    f = f_calculator(the_diameter, the_pipe_coefficient)
    Total_lost = minor_calculator(the_diameter) + major_calculator(f, the_diameter)
    velocity = velocity_calculator(the_diameter)
    area = area_calculator(the_diameter)
    mass_flowrate = density*velocity*area
    work_flow_pump = (gravitational_acceleration*elevation_difference_h2 + Total_lost)/ pump_efficiency
    pump_power = work_flow_pump*mass_flowrate/1000 # 1/1000 for W TO KW
    if 1<pump_power<2500:
        return pump_power
    else:
        #print("Pump power is not between desire range. Diameter: {} ".format(the_diameter))
        return None
def cost_calculator(the_pipe_coefficient , the_diameter):
    pump_power = pump_power_calculator(the_pipe_coefficient,the_diameter)
    if pump_power is None:
        return -1
    C_pump = 920 + 600*(pump_power**0.70)
    C_pipe = 800 * (the_diameter**0.74) * Lenght
    cost = C_pump+C_pipe
    return cost
lowest_cost_list = []
for the_pipe,the_pipe_coefficient in pipe_types.items() :

    for the_diameter in pipe_diameters:
        cost = cost_calculator(the_pipe_coefficient, the_diameter)
        if cost == -1:
            pass
        else:
            lowest_cost_list.append((the_pipe,the_diameter, cost))

sorted_data = sorted(lowest_cost_list, key=lambda x: x[2])
i = 1
for pipe_type,pipe_diameter,last_cost in sorted_data:
    number_str = f"{last_cost:.2f}"
    if '.' in number_str:
        integer_part, decimal_part = number_str.split('.')
        integer_part_with_dots = ".".join([integer_part[max(i - 3, 0):i] for i in range(len(integer_part), 0, -3)][::-1])
    else:
        integer_part = number_str
        decimal_part = '00'
        integer_part_with_dots = ".".join([integer_part[max(i - 3, 0):i] for i in range(len(integer_part), 0, -3)][::-1])
    formatted_number = f"{integer_part_with_dots},{decimal_part}"
    print("{})Pipe Type: {}, Pipe Diameter: {} meter, Cost: {}$\n ".format(i,pipe_type,pipe_diameter,formatted_number))
    i = i +1


