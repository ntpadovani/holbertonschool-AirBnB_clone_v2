import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.base_model import BaseModel
from models import storage


class TestConsole(unittest.TestCase):

    def setUp(self):
        self.console = HBNBCommand()

    def tearDown(self):
        storage.reload()

    """Test for do_create()"""
    @patch('sys.stdout', new_callable=StringIO)
    def test_do_create(self, mock_stdout):
        cmd = HBNBCommand()
        cmd.do_create("BaseModel")
        id = mock_stdout.getvalue().strip()
        self.assertTrue(len(id) > 0)
        self.assertIsInstance(cmd.classes['BaseModel'].all()[0], BaseModel)

        cmd.do_create("BaseModel name='test'")
        id = mock_stdout.getvalue().strip()
        self.assertTrue(len(id) > 0)
        objs = cmd.classes['BaseModel'].all()
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[1].name, 'test')

        cmd.do_create("BaseModel name=test number=123")
        id = mock_stdout.getvalue().strip()
        self.assertTrue(len(id) > 0)
        objs = cmd.classes['BaseModel'].all()
        self.assertEqual(len(objs), 3)
        self.assertEqual(objs[2].name, 'test')
        self.assertEqual(objs[2].number, 123)

    """Test for do_show()"""
    @patch('sys.stdout', new_callable=StringIO)
    def test_do_show_missing_class_name(self, mock_stdout):
        self.console.do_show('')
        self.assertEqual(mock_stdout.getvalue().strip(), '** class name missing **')

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_show_nonexistent_class(self, mock_stdout):
        self.console.do_show('MyModel')
        self.assertEqual(mock_stdout.getvalue().strip(), "** class doesn't exist **")

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_show_missing_instance_id(self, mock_stdout):
        self.console.do_show('BaseModel')
        self.assertEqual(mock_stdout.getvalue().strip(), '** instance id missing **')

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_show_nonexistent_instance(self, mock_stdout):
        self.console.do_show('BaseModel 123456')
        self.assertEqual(mock_stdout.getvalue().strip(), '** no instance found **')

    """Test do_destroy()"""
    def test_do_destroy_with_missing_class_name(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.console.onecmd('destroy')
            expected_output = "** class name missing **\n"
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_do_destroy_with_nonexistent_class_name(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.console.onecmd('destroy MyModel')
            expected_output = "** class doesn't exist **\n"
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_do_destroy_with_missing_instance_id(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.console.onecmd('destroy BaseModel')
            expected_output = "** instance id missing **\n"
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_do_destroy_with_nonexistent_instance_id(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.console.onecmd('destroy BaseModel 1234')
            expected_output = "** no instance found **\n"
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_do_destroy_with_valid_arguments(self):
        instance = BaseModel()
        storage.new(instance)
        storage.save()
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.console.onecmd('destroy BaseModel {}'.format(instance.id))
            self.assertEqual(fake_output.getvalue(), "")
        self.assertIsNone(storage.get('BaseModel', instance.id))

    """Test do_all()"""
    @patch('sys.stdout', new_callable=StringIO)
    def test_do_all_no_args(self, mock_stdout):
        self.console.onecmd("create BaseModel")
        self.console.onecmd("create User")
        self.console.onecmd("all")
        expected_output = "[BaseModel" in mock_stdout.getvalue() and "[User" in mock_stdout.getvalue()
        self.assertTrue(expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_all_with_args(self, mock_stdout):
        self.console.onecmd("create BaseModel")
        self.console.onecmd("create User")
        self.console.onecmd("all User")
        expected_output = "[User" in mock_stdout.getvalue() and "BaseModel" not in mock_stdout.getvalue()
        self.assertTrue(expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_all_invalid_class(self, mock_stdout):
        self.console.onecmd("all MyModel")
        expected_output = "** class doesn't exist **\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    """Test do_update()"""
    def test_do_update_error_missing_class_name(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual("** class name missing **\n", f.getvalue())

    def test_do_update_error_invalid_class_name(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_do_update_error_missing_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update BaseModel")
            self.assertEqual("** instance id missing **\n", f.getvalue())

    def test_do_update_error_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update BaseModel my_id")
            self.assertEqual("** no instance found **\n", f.getvalue())

    def test_do_update_error_missing_attribute_name(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"update BaseModel {self.b1.id}")
            self.assertEqual("** attribute name missing **\n", f.getvalue())

    def test_do_update_error_missing_attribute_value(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"update BaseModel {self.b1.id} name")
            self.assertEqual("** value missing **\n", f.getvalue())

    def test_do_update_error_invalid_attribute_name(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"update BaseModel {self.b1.id} invalid_attr val")
            self.assertEqual("", f.getvalue())

    def test_do_update(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"update BaseModel {self.b1.id} name test")
            self.assertEqual("", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show BaseModel {self.b1.id}")
            self.assertIn("test", f.getvalue())

    def test_do_update_with_dict(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"update BaseModel {self.b1.id} {{'name': 'test', 'age': 30}}")
            self.assertEqual("", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show BaseModel {self.b1.id}")
            self.assertIn("test", f.getvalue())
            self.assertIn("30", f.getvalue())


if __name__ == '__main__':
    unittest.main()