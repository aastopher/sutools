import sutools as su
from sutools import bench_handler


##### Methods

def test_benchy_and_register():
    benchy = bench_handler.Benchy()

    @su.register
    @benchy
    def func_add(x: int, y: int) -> int:
        """this is a test function"""
        return x + y

    @benchy
    @su.register
    def func_minus(x: int, y: int) -> int:
        """this is a test function"""
        return x - y
    
    @benchy
    @su.register
    def func_data(data: list) -> list:
        """this is a test function"""
        return data

    # call the functions
    func_add(1, 2)
    func_minus(2, 1)
    func_data(data=[1,2,3])

    # assert that reports were created\
    assert "func_add" in benchy.report
    assert "func_minus" in benchy.report
    assert "func_data" in benchy.report

    # assert that functions were registered
    assert "func_add" in su.store.funcs
    assert "func_minus" in su.store.funcs
    assert "func_data" in su.store.funcs

    # clear global registers
    su.benchy.report = {}
    su.store.funcs = {}