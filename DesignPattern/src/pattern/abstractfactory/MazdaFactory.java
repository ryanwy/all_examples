package pattern.abstractfactory;

/**
 * Created by Yan on 9/5/2016.
 */
public class MazdaFactory implements IFactory {
    @Override
    public IProductEngine createEngine(){
        return new ProductMazdaEngine();
    }

    @Override
    public IProductWheel createWheel(){
        return new ProductMazdaWheel();
    }
}
