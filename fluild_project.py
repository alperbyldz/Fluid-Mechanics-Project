import math
pipe_types = {
    'Riveted steel': 9.0,
    'Concrete': 3.0,
    'Wood stave': 0.18,
    'Cast iron': 0.26,
    'Galvanized iron': 0.15,
    'Commerical steel - Wrought iron': 0.045,
    'Drawn tubing': 0.0015,
    'Plastic - Glass': 0,
}
pipe_diameters = [0.015, 0.020, 0.025, 0.040, 0.050, 0.080, 0.100, 0.125,0.150,0.200,0.250,0.300,] # in meter
electric_cost = 0.04 # dolar/KW
flow_rate = 0.0139 # m^3/s
KL_minor_total = 9.05
pump_efficiency = 70/100
Lenght = 10000 # meter
viscosity = 2.9825*10**-4 # Ns/m^2
density = 961.85 #Kg/m^3
gravitational_acceleration = 9.81 # m/s^2
elevation_difference_h2 = 20 # meter
total_year=20
total_hour = total_year*365*24
P_vapor = 84926.4 #Pa
P_0 = 200000#Pa
NPSHr = 2
Pump_Kw = 2.2
Pump_Kw_Work = Pump_Kw*pump_efficiency
def area_calculator(the_diameter):
    area = (math.pi*(the_diameter**2))/4
    return area
def velocity_calculator(the_diameter):
    area = area_calculator(the_diameter)
    velocity = flow_rate/area
    return velocity
def reynolds_number_calculator(the_diameter,velocity):
    reynolds_number = (density*velocity*the_diameter)/viscosity
    return reynolds_number
def minor_calculator(the_diameter,velocity):
    minor = KL_minor_total*(velocity**2)/2
    return minor
def major_calculator(the_diameter,coefficent,velocity):
    f = f_calculator(the_diameter, coefficent,velocity)
    major = (f*(Lenght/the_diameter)*(velocity**2))/2
    return major
def f_calculator(the_diameter,coefficent,velocity):
    Re_number = reynolds_number_calculator(the_diameter,velocity)
    f = (1 / (-1.8 * math.log10((coefficent / the_diameter) / 3.7 + (6.9 / Re_number)))) ** 2
    return f
def pump_power_calculator(the_diameter,coefficent):
    velocity = velocity_calculator(the_diameter)
    Total_lost = minor_calculator(the_diameter,velocity) + major_calculator(the_diameter,coefficent,velocity)
    area = area_calculator(the_diameter)
    mass_flowrate = density*velocity*area
    work_flow_pump = (gravitational_acceleration*elevation_difference_h2 + Total_lost)/ pump_efficiency
    pump_power = work_flow_pump*mass_flowrate/1000 # 1/1000 for W TO KW
    pump_power = pump_power/pump_efficiency #danış
    if 1<pump_power<2500:
        totol_pump_number = pump_power/Pump_Kw
        pump_seperation_meter = Lenght/totol_pump_number
        return pump_power, totol_pump_number ,pump_seperation_meter
    else:
        return None, None, None
def cost_calculator(the_pipe_coefficient , the_diameter):
    pump_power, totol_pump_number ,pump_seperation_meter = pump_power_calculator(the_diameter,the_pipe_coefficient)
    if pump_power is None:
        return -1, None, None, None
    number_str = f"{totol_pump_number:.99f}"
    if '.' in number_str:
        integer_part, decimal_part = number_str.split('.')
        decimal_part_float = float("0."+decimal_part)
        totol_pump_number -=decimal_part_float
        totol_pump_number +=1
    C_electricity = electric_cost*pump_power*total_hour
    C_pump = 920 + 600*(pump_power**0.70)
    C_pipe = 800 * (the_diameter**0.74) * Lenght
    cost = C_pump+C_pipe+C_electricity
    return cost,pump_power,totol_pump_number, pump_seperation_meter
lowest_cost_list = []
for the_pipe,the_pipe_coefficient in pipe_types.items() :
    for the_diameter in pipe_diameters:
        (cost,power,number_of_pumps,seperation_distance) = cost_calculator(the_pipe_coefficient, the_diameter)
        if cost == -1:
            pass
        else:
            lowest_cost_list.append((the_pipe, the_diameter, cost, power,number_of_pumps,seperation_distance,the_pipe_coefficient ))
sorted_data = sorted(lowest_cost_list, key=lambda x: x[2])
i = 1
for pipe_type,pipe_diameter,last_cost,power_1,number_of_pump,seperation_distance,the_pipe_coefficient in sorted_data:
    if last_cost < 200000000000:
        number_str = f"{last_cost:.2f}"
        if '.' in number_str:
            integer_part, decimal_part = number_str.split('.')
            integer_part_with_dots = ".".join([integer_part[max(i - 3, 0):i] for i in range(len(integer_part), 0, -3)][::-1])
        else:
            integer_part = number_str
            decimal_part = '00'
            integer_part_with_dots = ".".join([integer_part[max(i - 3, 0):i] for i in range(len(integer_part), 0, -3)][::-1])
        formatted_number = f"{integer_part_with_dots},{decimal_part}"
        print("{})Pipe Type: {}, Pipe Diameter: {} meter, Cost: {}, $, Power : {}Kw, Number of pump {}, Pipe Coefficient : {}".format(i,pipe_type,pipe_diameter,formatted_number,power_1,number_of_pump, the_pipe_coefficient))
        i = i +1
    else:
        continue
print("***********************************************************************************************************************************************************************************************************************")
#Pipe systems values
#4)Pipe Type: Plastic - Glass, Pipe Diameter: 0.125 meter, Cost: 1.751.954,73, $, Power : 16.875791635587266Kw, Number of pump 11.0, Pump distance : 912.5497832957863 meter , Pipe Coefficient : 0
P_1 = 0
P_2 = 0
P_3 = 0
P_4 = 0
P_5 = 0
P_6 = 0
P_7 = 0
P_8 = 0
P_9 = 0
P_10 = 0
P_11= 0
P_12= 0
P_13 = 0
P_14 = 0
voted_diameter = 0.125
voted_pipe_type =  "Plastic - Glass"
voted_coefficient = 0
pipe_system_values = [[0.75,0,999,P_0],[1.76,0,1000,P_1],[0.64,0,1000,P_2],[0,0,1000,P_3],
                      [0.80,0,990,P_4],[0.48,0,750,P_5],[0.48,0,750,P_7],[1,0,750,P_8],[1,0,750,P_9],[0.4,0,1000,P_10],[0.4,0,1000,P_11],[1.19,20,20,P_12],[0.15,0,1,P_13]] # kl values , elevation difference , distance , Pressure
def HL_i_calculator(the_diameter,Kli,distance,velocity,coefficent):
    f = f_calculator(the_diameter,coefficent,velocity)
    hl_i = (Kli + f*(distance/the_diameter))*((velocity**2)/(2*gravitational_acceleration))
    return hl_i
def NPSHa_i_calculator(pump_number,velocity,Pi,elevation_difference_i,hl_i):
    NPSHa = (Pi/(density*gravitational_acceleration)+((velocity**2)/(2*gravitational_acceleration))+elevation_difference_i-hl_i-(P_vapor/(density*gravitational_acceleration)))
    if NPSHa <= NPSHr:
        print("NPSHa is less than NPSHr, Cavitation will occour at {} pump".format(pump_number))
        print("NPSHa : {} , NPSHr : {} ".format(NPSHa,NPSHr))
    else:
        print("NPSHa : {} , NPSHr : {} , Pump : {}".format(NPSHa, NPSHr,pump_number))
    return NPSHa
def pressure_after_pump(pump_number,Pi,elevation_difference_i,hl_i,the_diameter,coefficent,distance):
    if pump_number == len(pipe_types)-2:
        elevation_difference_i = pipe_system_values[len(pipe_system_values)-1][2]
        velocity = velocity_calculator(the_diameter)
        Kli_exit = pipe_system_values[len(pipe_system_values)-1][0]
        hl_i_exit = HL_i_calculator(the_diameter,Kli_exit,distance,velocity,coefficent)
        P_i_plus_1 = ( (Pi/gravitational_acceleration) - (elevation_difference_i*gravitational_acceleration) - hl_i_exit + ((Pump_Kw*pump_efficiency)/(density*flow_rate)))*gravitational_acceleration
        return P_i_plus_1
    else:
        P_i_plus_1 = (Pi/density+elevation_difference_i+((Pump_Kw*pump_efficiency)/(density*flow_rate))-hl_i)*density
        pipe_system_values[len(pipe_system_values)-1][3] = P_i_plus_1
    return P_i_plus_1
sayac = 0
for kl_values , elevation_difference , distance , Pressure in pipe_system_values:
    velocity = velocity_calculator(voted_diameter)
    hl_i = HL_i_calculator(the_diameter,kl_values,distance,velocity,voted_coefficient)
    new_pressure = pressure_after_pump(sayac,Pressure,elevation_difference,hl_i,voted_diameter,voted_coefficient,distance)
    sayac +=1
    pipe_system_values[sayac][3]   = new_pressure
    if sayac == len(pipe_system_values)-1:
        break
for i in pipe_system_values:
    print(i)
sayac = 1
print("")
for kl_values , elevation_difference , distance , Pressure in pipe_system_values:
    velocity = velocity_calculator(voted_diameter)
    hl_i = HL_i_calculator(voted_diameter,kl_values,distance,velocity,voted_coefficient)
    if sayac <= len(pipe_system_values)-1:
        NPSHa_i_calculator(sayac,velocity,Pressure,elevation_difference,hl_i)
        sayac+=1
print("***********************************************************************************************************************************************************************************************************************")
pump_power = (sayac-1)*Pump_Kw
C_electricity = electric_cost*pump_power*total_hour
C_pump = 920 + 600*(pump_power**0.70)
C_pipe = 800 * (voted_diameter**0.74) * Lenght
cost = C_pump+C_pipe+C_electricity
number_str = f"{cost:.2f}"
if '.' in number_str:
    integer_part, decimal_part = number_str.split('.')
    integer_part_with_dots = ".".join([integer_part[max(i - 3, 0):i] for i in range(len(integer_part), 0, -3)][::-1])
else:
    integer_part = number_str
    decimal_part = '00'
    integer_part_with_dots = ".".join([integer_part[max(i - 3, 0):i] for i in range(len(integer_part), 0, -3)][::-1])
formatted_number = f"{integer_part_with_dots},{decimal_part}"
print("Actual cost: {} $".format(formatted_number))
