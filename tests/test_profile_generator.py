import unittest
from pathlib import Path

from tools.profile import generate


class ProfileGeneratorTests(unittest.TestCase):
    def test_city_generation_is_deterministic(self):
        sample = [{"date": f"2026-01-{(i % 28) + 1:02d}", "count": i % 9} for i in range(365)]
        first = generate.generate_contribution_city_svg(sample)
        second = generate.generate_contribution_city_svg(sample)
        self.assertEqual(first, second)

    def test_normalize_fallback_for_malformed_data(self):
        fallback = generate.normalize_contributions([{"date": "bad-date", "contributionCount": "n/a"}])
        self.assertEqual(len(fallback), 365)
        self.assertTrue(all("date" in item and "count" in item for item in fallback))

    def test_all_project_links_present_in_readme(self):
        config = {
            "github_username": "Shikhyy",
            "display_name": "Shikhyy",
            "role": "Role",
            "pitch": "Pitch",
            "social": {
                "github": "https://github.com/Shikhyy",
                "dev": "https://dev.to/your-dev-username",
                "linkedin": "https://www.linkedin.com/in/your-linkedin",
                "x": "https://x.com/your-x-handle",
                "youtube": "https://www.youtube.com/@your-channel",
                "discord": "https://discord.com/users/your-user-id",
            },
            "dev": {"enabled": False, "username": ""},
        }
        projects = [
            generate.Project(
                name=name,
                url=f"https://github.com/Shikhyy/{name}",
                description="Description not provided in repository metadata.",
            )
            for name in generate.ALL_PROJECT_NAMES
        ]
        generate.build_readme(config, projects, None, [])

        readme = Path(generate.ROOT / "README.md").read_text(encoding="utf-8")
        for name in generate.ALL_PROJECT_NAMES:
            self.assertIn(f"https://github.com/Shikhyy/{name}", readme)

    def test_svg_outputs_have_titles(self):
        generate.run()
        targets = [
            generate.ASSETS_DIR / "header.svg",
            generate.ASSETS_DIR / "stats.svg",
            generate.ASSETS_DIR / "contribution-city.svg",
            generate.ASSETS_DIR / "stack.svg",
            generate.ASSETS_DIR / "footer.svg",
        ]
        for file_path in targets:
            content = file_path.read_text(encoding="utf-8")
            self.assertIn("<svg", content)
            self.assertIn("<title", content)


if __name__ == "__main__":
    unittest.main()
