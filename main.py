from abc import ABC, abstractmethod

class RecyclingPlantFactory(ABC):
    @abstractmethod
    def create_machine(self):
        pass

    @abstractmethod
    def create_sorting_module(self):
        pass


class WastePlantA(RecyclingPlantFactory):
    def create_machine(self):
        return MachineA()

    def create_sorting_module(self):
        return SortingModuleA()


class WastePlantB(RecyclingPlantFactory):
    def create_machine(self):
        return MachineB()

    def create_sorting_module(self):
        return SortingModuleB()


class Machine(ABC):
    @abstractmethod
    def process_waste(self, waste):
        pass


class MachineA(Machine):
    def process_waste(self, waste):
        if waste.type == "plastic":
            return 0.3*waste.amount
        elif waste.type == "paper":
            return 0.4*waste.amount
        elif waste.type == "glass":
            return 0.5*waste.amount
        else:
            return 0.3*waste.amount


class MachineB(Machine):
    def process_waste(self, waste):
        if waste.type == "plastic":
            return 0.2 * waste.amount
        elif waste.type == "paper":
            return 0.45 * waste.amount
        elif waste.type == "glass":
            return 0.3 * waste.amount
        else:
            return 0.25 * waste.amount


class SortingModule(ABC):
    @abstractmethod
    def sort_waste(self, waste):
        pass


class SortingModuleA(SortingModule):
    def sort_waste(self, waste):
        if waste.type == "plastic":
            waste.amount *= 0.9
        elif waste.type == "paper":
            waste.amount *= 0.93
        elif waste.type == "glass":
            waste.amount *= 0.65
        else:
            waste.amount *= 0.5
        return waste


class SortingModuleB(SortingModule):
    def sort_waste(self, waste):
        if waste.type == "plastic":
            waste.amount *= 0.8
        elif waste.type == "paper":
            waste.amount *= 0.95
        elif waste.type == "glass":
            waste.amount *= 0.7
        else:
            waste.amount *= 0.65
        return waste


class Waste:
    def __init__(self, amount, type):
        self.amount = amount
        self.type = type


class RecyclingPlant:
    def __init__(self, factory):
        self.factory = factory
        self.machine = factory.create_machine()
        self.sorting_module = factory.create_sorting_module()
        self.recyclable_material = 0.0
        self.count_of_resources = 100

    def process_waste(self, waste):
        if self.count_of_resources >= 1:
            waste = self.sorting_module.sort_waste(waste)
            self.recyclable_material += self.machine.process_waste(waste)
            self.count_of_resources -= 1
        else:
            print("Alas... Not enough resources for recycling")

    def transfer_material(self, other_plant):
        other_plant.recyclable_material += self.recyclable_material
        self.recyclable_material = 0.0


def process(rp):
    amount = float(input("Enter the amount of garbage: "))
    type = input("Enter the type of garbage: ")
    w = Waste(amount, type)
    rp.process_waste(w)
    print("The received material: " + str(rp.recyclable_material))


rp1 = RecyclingPlant(WastePlantA())
rp2 = RecyclingPlant(WastePlantB())

while True:
    ans = int(input("Choose a waste recycling factory: 1.A; 2.B; 0. Exit - "))
    if ans == 1:
        rp = rp1
        process(rp)
        a = input("Do you want to send the recycled material to another factory? y/n: ")
        if a == "y":
            rp.transfer_material(rp2)
            print("Materials have been sent")
            print("Recycled material located at the factory A: " + str(rp1.recyclable_material))
            print("Recycled material located at the factory B: " + str(rp2.recyclable_material))
    elif ans == 2:
        rp = rp2
        process(rp)
        a = input("Do you want to send the recycled material to another factory? y/n: ")
        if a == "y":
            rp.transfer_material(rp1)
            print("Materials have been sent")
            print("Recycled material located at the factory A: " + str(rp1.recyclable_material))
            print("Recycled material located at the factory B: " + str(rp2.recyclable_material))
    elif ans == 0:
        break
    else:
        print("!--Choose 1 or 2--!")