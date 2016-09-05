package pattern.abstractfactory;

/**
 * Created by Yan on 9/5/2016.
 */
public interface IFactory {
    IProductEngine createEngine();
    IProductWheel createWheel();
}
