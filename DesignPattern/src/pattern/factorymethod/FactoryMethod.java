package pattern.factorymethod;

/**
 * Created by Yan on 8/30/2016.
 * 工厂方法模式，即工厂模式，是gof 23种设计模式之一，创建型模式
 * 它是对简单工厂模式的改进，避免简单工厂模式中过重依赖工厂类，这里抽象出一个工厂接口，要新增什么产品，只需要继承这个工厂接口和一个产品接口，
 * 从而遵从了开放封闭原则，可扩展性更好
 * 工厂方法，一个抽象工厂，派生出多个工厂，一个抽象产品，派生出多个产品；一个工厂负责对应的具体的产品
 *
 * client-工厂抽象 - 工厂实现1 - 产品抽象 - 产品实现1
 *       -工厂抽象 - 工厂实现2 - 产品抽象 - 产品实现2
 *
 */
public class FactoryMethod {
    public static void main(String[] args) throws Exception {
        Factories fac = new BmwFactory();
        Cars car = fac.produce();
        car.printStyle();

        Factories fac2 = new MazdaFactory();
        Cars car2 = fac2.produce();
        car2.printStyle();
    }
}
