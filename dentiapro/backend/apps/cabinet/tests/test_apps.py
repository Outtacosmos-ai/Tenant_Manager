from cabinet.apps import CabinetConfig

def test_cabinet_config_name():
    cabinet_config = CabinetConfig()
    assert cabinet_config.name == 'cabinet'
