from unittest.mock import patch
from http import HTTPStatus


def test_log_action_invalid_action(client, jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/api/invalid_action", headers=headers, json={})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.get_json() == {"msg": "Invalid action"}


@patch("src.routes.producer")
def test_log_action_valid_action(mock_producer, client, jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}

    for action in ["click", "view", "quality_change", "video_progress", "query"]:
        response = client.post(f"/api/{action}", headers=headers, json={"key": "value"})
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"msg": f"{action.capitalize()} logged"}
        mock_producer.send.assert_called_with(
            topic=f"{action}_events",
            value={"user": "test_user", "action": action, "data": {"key": "value"}},
        )
