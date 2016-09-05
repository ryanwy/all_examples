package pattern.abstractfactory;

/**
 * Created by Yan on 9/5/2016.
 * 抽象工厂模式，属于gof 23中设计模式之一，创建型模式
 * 一般说抽象工厂模式是工厂方法模式的抽象，而且在实际中比较难以分辨。主要的区别如同例子中显示的：
 * 工厂方法模式只有一个抽象产品类，一个抽象工厂类，对应多个具体的产品实现类和多个具体的工厂实现类
 * 抽象工厂模式既然是升级，有多个抽象产品类和一个抽象工厂类,对应多个具体产品实现类和具体工厂实现类
 *
 *
 */
public class AbstractFactory {

    public static void main(String[] argv) {
        IFactory fac = new BmwFactory();
        fac.createEngine().printProduct();
        fac.createWheel().printProduct();
        IFactory fac2 = new MazdaFactory();
        fac2.createEngine().printProduct();
        fac2.createWheel().printProduct();
    }
}
