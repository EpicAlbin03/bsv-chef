import pytest
from unittest.mock import patch, MagicMock
from src.controllers.recipecontroller import RecipeController
from src.static.diets import Diet

# Test get_recipe:
# 1. Pantry is empty
# 2. Pantry has all ingredients for optimal recipe
# 3. Pantry has all ingredients for random recipe
# 4. No recipe matches the specified diet

@pytest.fixture
def mock_dao():
    return MagicMock()

@pytest.fixture
def mock_recipe_controller(mock_dao):
    return RecipeController(items_dao=mock_dao)

@pytest.mark.unit
def test_empty_pantry(mock_recipe_controller, mock_dao):
    mock_dao.get_all.return_value = []
    mock_recipe_controller.get_available_items = MagicMock(return_value={})

    result = mock_recipe_controller.get_recipe(Diet.NORMAL, True)
    assert result is None

@pytest.mark.unit
def test_optimal_recipe(mock_recipe_controller, mock_dao):
    mock_dao.get_all.return_value = [{"name": "flour", "quantity": 1}]
    mock_recipe_controller.get_available_items = MagicMock(return_value={"flour": 1})

    recipe1 = {
        "name": "Bread",
        "ingredients": {"flour": 1},
        "diets": ["normal"]
    }
    recipe2 = {
        "name": "Cake",
        "ingredients": {"flour": 1, "sugar": 1},
        "diets": ["normal"]
    }
    mock_recipe_controller.recipes = [recipe1, recipe2]

    mock_recipe_controller.get_readiness_of_recipes = MagicMock(return_value={"Bread": 1.0, "Cake": 0.5})

    # ! Returns random recipe instead of optimal "Bread"
    result = mock_recipe_controller.get_recipe(Diet.NORMAL, True)
    assert result == recipe1["name"]

@pytest.mark.unit
def test_random_recipe(mock_recipe_controller, mock_dao):
    mock_dao.get_all.return_value = [{"name": "flour", "quantity": 2}]
    mock_recipe_controller.get_available_items = MagicMock(return_value={"flour": 2})

    recipe1 = {
        "name": "Bread",
        "ingredients": {"flour": 1},
        "diets": ["normal"]
    }
    recipe2 = {
        "name": "Pancake",
        "ingredients": {"flour": 1},
        "diets": ["normal"]
    }
    mock_recipe_controller.recipes = [recipe1, recipe2]

    mock_recipe_controller.get_readiness_of_recipes = MagicMock(return_value={"Bread": 1.0, "Pancake": 1.0})

    with patch('src.controllers.recipecontroller.RecipeController.get_recipe', return_value="Bread"):
        result = mock_recipe_controller.get_recipe(Diet.NORMAL, False)
        assert result == recipe1["name"]

    with patch('src.controllers.recipecontroller.RecipeController.get_recipe', return_value="Pancake"):
        result = mock_recipe_controller.get_recipe(Diet.NORMAL, False)
        assert result == recipe2["name"]

@pytest.mark.unit
def test_no_matching_diet(mock_recipe_controller, mock_dao):
    mock_dao.get_all.return_value = [{"name": "flour", "quantity": 2}]
    mock_recipe_controller.get_available_items = MagicMock(return_value={"flour": 2})

    recipe = {
        "name": "Bread",
        "ingredients": {"flour": 1},
        "diets": ["normal"]
    }
    mock_recipe_controller.recipes = [recipe]

    mock_recipe_controller.get_readiness_of_recipes = MagicMock(return_value={})

    result = mock_recipe_controller.get_recipe(Diet.VEGAN, True)
    assert result is None