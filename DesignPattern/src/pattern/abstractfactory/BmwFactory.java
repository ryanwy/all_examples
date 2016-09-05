package pattern.abstractfactory;

/**
 * Created by Yan on 9/5/2016.
 */
public class BmwFactory implements IFactory {
    @Override
    public IProductEngine createEngine(){
        return new ProductBmwEngine();
    }

    @Override
    public IProductWheel createWheel(){
        return new ProductBmwWheel();
    }
}
