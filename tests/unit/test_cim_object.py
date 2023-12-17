from project_manager.cim_object import CimObject


def test_validate_class_creation(init_cim_object):
    cim_object = init_cim_object
    assert cim_object.ClassID == "ANALOG"
    assert cim_object.ID == "ANALOG_TEST"
    assert cim_object.Attributes == [
        {
            "ID": "OPC_CHANNEL",
            "Value": "OPC"
        },
        {
            "ID": "$DEVICE_ID",
            "Value": "PANEL_MAIN"
        },
        {
            "ID": "CAPTION",
            "Value": "Analog"
        },
        {
            "ID": "$SCREEN_ID",
            "Value": "Analog"
        },
        {
            "ID": "$RESOURCE_ID",
            "Value": "$SYSTEM"
        },
        {
            "ID": "SP_EX",
            "Value": "1"
        },
        {
            "ID": "OPC_DEVICE",
            "Value": "OPC"
        },
        {
            "ID": "COMMENT",
            "Value": "Analog"
        }
    ]
    assert cim_object.Description == "Analog test"
    assert cim_object.Routing == []


def test_cim_object_to_dict(init_cim_object):
    cim_object_dict = init_cim_object.to_dict()
    assert isinstance(cim_object_dict, dict)
    assert cim_object_dict == {
        "Attributes": [
            {
                "ID": "OPC_CHANNEL",
                "Value": "OPC"
            },
            {
                "ID": "$DEVICE_ID",
                "Value": "PANEL_MAIN"
            },
            {
                "ID": "CAPTION",
                "Value": "Analog"
            },
            {
                "ID": "$SCREEN_ID",
                "Value": "Analog"
            },
            {
                "ID": "$RESOURCE_ID",
                "Value": "$SYSTEM"
            },
            {
                "ID": "SP_EX",
                "Value": "1"
            },
            {
                "ID": "OPC_DEVICE",
                "Value": "OPC"
            },
            {
                "ID": "COMMENT",
                "Value": "Analog"
            }
        ],
        "ClassID": "ANALOG",
        "Description": "Analog test",
        "ID": "ANALOG_TEST",
        "Routing": []
    }


def test_cim_object_equality(init_cim_object):
    # Create another instance with the same data
    cim_obj = CimObject([
        {
            "ID": "OPC_CHANNEL",
            "Value": "OPC"
        },
        {
            "ID": "$DEVICE_ID",
            "Value": "PANEL_MAIN"
        },
        {
            "ID": "CAPTION",
            "Value": "Analog"
        },
        {
            "ID": "$SCREEN_ID",
            "Value": "Analog"
        },
        {
            "ID": "$RESOURCE_ID",
            "Value": "$SYSTEM"
        },
        {
            "ID": "SP_EX",
            "Value": "1"
        },
        {
            "ID": "OPC_DEVICE",
            "Value": "OPC"
        },
        {
            "ID": "COMMENT",
            "Value": "Analog"
        }
    ], "ANALOG", "Analog test", "ANALOG_TEST", [])

    assert init_cim_object == cim_obj


def test_cim_object_inequality(init_cim_object):
    # Create another instance with different data
    different_cim_class = CimObject([
        {
            "ID": "OPC_CHANNEL",
            "Value": "OPC"
        },
        {
            "ID": "$DEVICE_ID",
            "Value": "PANEL_MAIN"
        }], "VALVE", "Valve test", "VALVE_TEST", [])

    assert init_cim_object != different_cim_class
