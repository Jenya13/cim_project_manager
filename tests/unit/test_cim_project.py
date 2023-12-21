import pytest
import os
import shutil
from tests.settings.configs import project_name
from datetime import datetime, timedelta
from project_manager.cim_project import CimProject
from project_manager.cim_class import CimClass
from project_manager.cim_object import CimObject
from tools.configs_editor import read_config


@pytest.mark.project
def test_validate_project_creation():
    project = CimProject()
    project.init_project("TG1")
    assert project.project_id == "TG1"
    assert project.session_manager is not None
    assert len(project.cim_classes) > 0
    assert len(project.cim_objects) > 0

    projects_dir = read_config("USER", "projects_dir")
    project_dir = os.path.join(projects_dir, project.project_id)
    settings_dir = os.path.join(project_dir, "settings")
    templates_dir = os.path.join(project_dir, "templates")
    updates_dir = os.path.join(project_dir, "updates")

    assert os.path.exists(project_dir)
    assert os.path.exists(settings_dir)
    assert os.path.exists(templates_dir)
    assert os.path.exists(updates_dir)

    settings_file = os.path.join(settings_dir, f"{project.project_id}.json")
    current_time = datetime.now()
    current_time_str = current_time.strftime("%d-%m-%Y_%H-%M")
    template_file = os.path.join(
        templates_dir, f"{project.project_id}_{current_time_str}.xlsx")

    assert os.path.isfile(settings_file)
    assert os.path.isfile(template_file)
    shutil.rmtree(project_dir)


@pytest.mark.project
def test_validate_substring_correctness(init_project):
    project = init_project
    invalid_input = project._extract_substring("Hello world!")
    valid_input = project._extract_substring("Hello world! #[SP]")
    NoneType = type(None)
    assert isinstance(invalid_input, NoneType)
    assert invalid_input is None
    assert isinstance(valid_input, str)
    assert valid_input == "SP"


@pytest.mark.project
def test_validate_getting_classes(init_project):
    project = init_project
    project_id = project.project_id
    session = project.session_manager.to_dict()
    classes = project._get_classes(project_id, session)
    assert isinstance(classes, list)
    for cls in classes:
        assert isinstance(cls, CimClass)


@pytest.mark.project
def test_validate_getting_objects(init_project):
    project = init_project
    project_id = project.project_id
    session = project.session_manager.to_dict()
    object_id = "*_TEST"
    params = {"projectId": project_id, "ObjectID": object_id}
    objects = project._get_objects(project_id, session, params)
    assert isinstance(objects, list)
    for obj in objects:
        assert isinstance(obj, CimObject)


@pytest.mark.project
def test_validate_template_file_creation(init_project):
    project = init_project
    projects_dir = read_config("USER", "projects_dir")
    project_dir = os.path.join(projects_dir, project.project_id)
    template_dir = os.path.join(project_dir, "templates")

    classes_list = []
    for cls in project.cim_classes:
        classes_list.append(cls.to_dict())

    objects_list = []
    for obj in project.cim_objects:
        objects_list.append(obj.to_dict())

    template_list = project.create_template_list(
        classes_list, objects_list)

    test_time = datetime.now()
    test_time_str = test_time.strftime("%d-%m-%Y_%H-%M")

    project.create_template_file(
        "test", project_dir, template_list)

    files = os.listdir(template_dir)
    files = [f for f in files if os.path.isfile(template_dir+'/'+f)]
    file_path = os.path.join(
        template_dir, f"test_{test_time_str}.xlsx")
    assert len(files) == 2
    assert os.path.isfile(file_path)
    os.remove(file_path)


@pytest.mark.project
def test_validation_project_is_set(init_project):
    project = CimProject()
    project.set_project(project_name)
    assert project.project_id == "TG1"
    assert project.session_manager is not None
    assert len(project.cim_classes) > 0
    assert len(project.cim_objects) > 0

    projects_dir = read_config("USER", "projects_dir")
    project_dir = os.path.join(projects_dir, project.project_id)
    settings_dir = os.path.join(project_dir, "settings")
    templates_dir = os.path.join(project_dir, "templates")
    updates_dir = os.path.join(project_dir, "updates")

    assert os.path.exists(project_dir)
    assert os.path.exists(settings_dir)
    assert os.path.exists(templates_dir)
    assert os.path.exists(updates_dir)

    settings_file = os.path.join(settings_dir, f"{project.project_id}.json")
    files = os.listdir(templates_dir)
    files = [f for f in files if os.path.isfile(templates_dir+'/'+f)]
    template_file = os.path.join(
        templates_dir, files[0])
    assert len(files) == 1

    assert os.path.isfile(settings_file)
    assert os.path.isfile(template_file)


# def test_validate_creation_template_list():
#     pass


# def test_validate_project_setting():
#     pass


# def test_validate_template_update():
#     pass
