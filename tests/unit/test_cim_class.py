from project_manager.cim_class import CimClass


def test_validate_class_creation(init_cim_class):
    cim_class = init_cim_class
    assert cim_class.classId == "ANALOG"
    assert cim_class.classVersion == 10
    assert cim_class.dataItems == [
        {
            "dataItemId": "SP",
            "dataType": "REAL",
            "description": "{$DESCRIPTION} - Setpoint Value #[SP_EX]"
        },
        {
            "dataItemId": "PV",
            "dataType": "REAL",
            "description": "{$DESCRIPTION} - Present Value #[PV_EX]"
        }
    ]
    assert cim_class.description == "Analog"
    assert cim_class.compositeMembers is None


def test_cim_class_to_dict(init_cim_class):
    cim_class_dict = init_cim_class.to_dict()
    assert isinstance(cim_class_dict, dict)
    assert cim_class_dict == {
        "classId": "ANALOG",
        "classVersion": 10,
        "dataItems": [
            {
                "dataItemId": "SP",
                "dataType": "REAL",
                "description": "{$DESCRIPTION} - Setpoint Value #[SP_EX]"
            },
            {
                "dataItemId": "PV",
                "dataType": "REAL",
                "description": "{$DESCRIPTION} - Present Value #[PV_EX]"
            }
        ],
        "description": "Analog",
        "compositeMembers": None
    }


def test_cim_class_equality(init_cim_class):
    # Create another instance with the same data
    same_cim_class = CimClass("ANALOG", 10, [
        {
            "dataItemId": "SP",
            "dataType": "REAL",
            "description": "{$DESCRIPTION} - Setpoint Value #[SP_EX]"
        },
        {
            "dataItemId": "PV",
            "dataType": "REAL",
            "description": "{$DESCRIPTION} - Present Value #[PV_EX]"
        }
    ], "Analog", None)

    assert init_cim_class == same_cim_class


def test_cim_class_inequality(init_cim_class):
    # Create another instance with different data
    different_cim_class = CimClass("DIGITAL", 5, [
        {
            "dataItemId": "SV",
            "dataType": "STRING",
            "description": "{$DESCRIPTION} - Setpoint Value #[SV_EX]"
        }
    ], "Digital", None)

    assert init_cim_class != different_cim_class


# def test_cim_class_string_representation(init_cim_class):
#     expected_str = "CimClass(classId='ANALOG', classVersion=10, dataItems=[{'dataItemId': 'SP', 'dataType': 'REAL', 'description': '{$DESCRIPTION} - Setpoint Value #[SP_EX]'}, {'dataItemId': 'PV', 'dataType': 'REAL', 'description': '{$DESCRIPTION} - Present Value #[PV_EX]'}], description='Analog', compositeMembers=None)"
#     assert str(init_cim_class) == expected_str
