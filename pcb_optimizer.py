import math
import random
import matplotlib.pyplot as plt

# --- 1. تمثيل البيانات (Data Structures) ---
class Component:
    def __init__(self, id, width, height, x=0, y=0):
        self.id = id
        self.w = width
        self.h = height
        self.x = x
        self.y = y

class Net:
    def __init__(self, id, components):
        self.id = id
        self.components = components  # قائمة بالكائنات من نوع Component

    def calculate_hpwl(self):
        # حساب نصف محيط المستطيل المحيط (HPWL)
        xs = [c.x + c.w/2 for c in self.components]
        ys = [c.y + c.h/2 for c in self.components]
        return (max(xs) - min(xs)) + (max(ys) - min(ys))

# --- 2. المحرك الرئيسي للمحسن (The Optimizer) ---
class PCBPlacementOptimizer:
    def __init__(self, components, nets, boundary_w, boundary_h):
        self.components = components
        self.nets = nets
        self.boundary_w = boundary_w
        self.boundary_h = boundary_h
        self.alpha = 500  # معامل عقوبة التداخل (Penalty)

    def total_cost(self):
        # 1. حساب طول الأسلاك
        hpwl_total = sum(net.calculate_hpwl() for net in self.nets)
        
        # 2. حساب التداخلات (Overlaps) - تبسيط للفهم
        overlap_penalty = 0
        for i, c1 in enumerate(self.components):
            for j, c2 in enumerate(self.components):
                if i >= j: continue
                # التحقق من التصادم بين المكونات
                dx = min(c1.x + c1.w, c2.x + c2.w) - max(c1.x, c2.x)
                dy = min(c1.y + c1.h, c2.y + c2.h) - max(c1.y, c2.y)
                if dx > 0 and dy > 0:
                    overlap_penalty += (dx * dy)
        
        return hpwl_total + (self.alpha * overlap_penalty)

    def optimize(self, initial_temp=1000, cooling_rate=0.95, iterations=1000):
        current_temp = initial_temp
        current_cost = self.total_cost()
        best_cost = current_cost
        
        history = []

        for i in range(iterations):
            # اختيار مكون عشوائي وتغيير مكانه
            comp = random.choice(self.components)
            old_x, old_y = comp.x, comp.y
            
            # حركة عشوائية (Perturbation)
            comp.x = max(0, min(self.boundary_w - comp.w, comp.x + random.uniform(-20, 20)))
            comp.y = max(0, min(self.boundary_h - comp.h, comp.y + random.uniform(-20, 20)))
            
            new_cost = self.total_cost()
            delta = new_cost - current_cost
            
            # معيار ميتوبوليس (Metropolis Criterion)
            if delta < 0 or random.random() < math.exp(-delta / current_temp):
                current_cost = new_cost
                if current_cost < best_cost:
                    best_cost = current_cost
            else:
                # التراجع عن الحركة
                comp.x, comp.y = old_x, old_y
            
            current_temp *= cooling_rate
            history.append(current_cost)
            
            if i % 100 == 0:
                print(f"Iteration {i}: Cost = {current_cost:.2f}, Temp = {current_temp:.2f}")

        return history

    def visualize(self):
        fig, ax = plt.subplots()
        for c in self.components:
            rect = plt.Rectangle((c.x, c.y), c.w, c.h, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            ax.text(c.x, c.y, str(c.id), fontsize=8)
        
        plt.xlim(0, self.boundary_w)
        plt.ylim(0, self.boundary_h)
        plt.title(f"Final PCB Layout (Best Cost Reached)")
        plt.show()

# --- 3. تشغيل تجريبي (Demo) ---
if __name__ == "__main__":
    # إنشاء مكونات وهمية
    c1 = Component(1, 10, 20, 5, 5)
    c2 = Component(2, 15, 15, 50, 50)
    c3 = Component(3, 20, 10, 80, 20)
    
    components = [c1, c2, c3]
    
    # إنشاء شبكات (Nets) تربط المكونات
    nets = [
        Net(101, [c1, c2]),
        Net(102, [c2, c3]),
        Net(103, [c1, c3])
    ]
    
    # تشغيل المحسن
    optimizer = PCBPlacementOptimizer(components, nets, 100, 100)
    history = optimizer.optimize(iterations=500)
    
    # عرض النتيجة
    optimizer.visualize()