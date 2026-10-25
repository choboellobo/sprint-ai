import importlib.util
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "skills" / "board" / "board.py"
spec = importlib.util.spec_from_file_location("sprint_board", MODULE_PATH)
board = importlib.util.module_from_spec(spec)
spec.loader.exec_module(board)


class BoardTests(unittest.TestCase):
    def test_demo_milestones_and_archived_sprints(self):
        project = Path(__file__).resolve().parents[1] / "examples" / "demo-project"

        state = board.load_state(project)

        self.assertEqual(state["id"], "SP-002")
        self.assertEqual([sprint["id"] for sprint in state["history"]], ["SP-001"])
        self.assertEqual(len(state["milestones"]), 3)
        self.assertEqual((state["milestones"][0]["done"], state["milestones"][0]["total"]), (1, 1))
        self.assertEqual((state["milestones"][1]["done"], state["milestones"][1]["total"]), (1, 5))
        self.assertNotIn("US-007", [item["id"] for item in state["items"]])

    def test_joins_sprint_with_backlog_and_reads_plan(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "plans").mkdir()
            (project / "BACKLOG.md").write_text(
                "## Backlog\n"
                "| ID | Story | Areas | Requires | Plan |\n"
                "| --- | --- | --- | --- | --- |\n"
                "| US-001 | Entrar en la cuenta | front, back | — | plans/US-001-login.md |\n"
                "| US-002 | Recuperar clave | front | US-001 | — |\n",
                encoding="utf-8",
            )
            (project / "SPRINT.md").write_text(
                "# Sprint: Acceso\n\nGoal: Entrar con seguridad\n\n## Board\n"
                "| ID | Story | Areas | Status | Plan | Next action |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                "| US-001 | Entrar en la cuenta | front, back | Waiting For | — | Elegir proveedor; resume: In Progress |\n",
                encoding="utf-8",
            )
            (project / "plans" / "US-001-login.md").write_text(
                "## Acceptance criteria\n- [ ] Se puede iniciar sesión.\n"
                "## Verification\n- [ ] Probar login en navegador.\n",
                encoding="utf-8",
            )

            state = board.load_state(project)

            self.assertEqual(state["sprint"], "Acceso")
            self.assertEqual(state["goal"], "Entrar con seguridad")
            self.assertEqual(state["counts"]["Waiting For"], 1)
            self.assertEqual(state["counts"]["Backlog"], 1)
            self.assertEqual(state["areas"], ["back", "front"])
            self.assertEqual(state["items"][0]["nextAction"], "Elegir proveedor; resume: In Progress")
            self.assertEqual(state["items"][0]["plan"]["criteria"], ["Se puede iniciar sesión."])
            self.assertEqual(state["items"][1]["status"], "Backlog")

    def test_legacy_numbered_backlog_works_without_sprint(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "BACKLOG.md").write_text(
                "## Backlog\n"
                "1. Como usuario, quiero añadir una tarea. Plan: plans/01.md\n"
                "1b. Como usuario, quiero ver un aviso. Requires: #1\n",
                encoding="utf-8",
            )

            state = board.load_state(project)

            self.assertFalse(state["hasSprint"])
            self.assertEqual([item["id"] for item in state["items"]], ["1", "1b"])
            self.assertEqual(state["counts"]["Backlog"], 2)
            self.assertEqual(state["items"][0]["story"], "Como usuario, quiero añadir una tarea.")

    def test_plan_path_cannot_escape_project(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            project.mkdir()
            outside = Path(directory) / "outside.md"
            outside.write_text("## Acceptance criteria\n- Secret\n", encoding="utf-8")

            details = board.plan_details(project, "../outside.md")

            self.assertEqual(details["criteria"], [])
            self.assertEqual(details["path"], "../outside.md")


if __name__ == "__main__":
    unittest.main()
