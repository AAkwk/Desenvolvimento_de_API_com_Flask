import pytest
from src.utils import eleva_quadrado , requires_role
from unittest.mock import  patch
from http import HTTPStatus



@pytest.mark.parametrize("test_input,expected", [(2, 4), (3, 9), (4, 16), (5, 25)])
def test_eleva_quadrado_parametrized(test_input, expected):
    assert eleva_quadrado(test_input) == expected



@pytest.mark.parametrize("test_input,exc_class,msg", [('a', TypeError, "can't multiply sequence by non-int of type 'str'"), (None, TypeError, "unsupported operand type(s) for *: 'NoneType' and 'NoneType'")])
def test_eleva_quadrado_exceptions(test_input, exc_class, msg):
    with pytest.raises(exc_class) as exc_info:
        eleva_quadrado(test_input)
    assert str(exc_info.value) == msg



def test_requires_role_sucess(mocker):
    #given
    mock_user = mocker.Mock()
    mock_user.role.name = 'admin'
    
    mocker.patch("src.utils.get_jwt_identity") 
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)   
    decorated_fuction = requires_role('admin')(lambda: "Success")
    #when
    result = decorated_fuction()
    #then
    assert result == "Success"

    

def test_requires_role_fail(mocker):
    #given
    mock_user = mocker.Mock()
    mock_user.role.name = 'normal'
    
    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
    decorated_fuction = requires_role('admin')(lambda: "Success")
    #when
    result = decorated_fuction()
    #then 
    assert result == ({"message":"Admin privilege required."}, HTTPStatus.FORBIDDEN)

    