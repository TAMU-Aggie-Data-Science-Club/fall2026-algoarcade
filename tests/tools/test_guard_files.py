import pytest

import guard_files


@pytest.mark.parametrize(
    "name",
    [
        "firered.gba",
        "roms/sml.GB",
        "save.sav",
        "s1.state",
        "quick.ss3",
        "pokefirered.sym",
        "layouts/PalletTown/map.bin",
        "data/runs/x.parquet",
        "data/roms/readme.txt",
    ],
)
def test_rejects_game_data_and_anything_under_data(name: str) -> None:
    assert guard_files.problem(name)


@pytest.mark.parametrize(
    "name",
    [
        "data/.gitkeep",
        "src/algoarcade/rom.py",
        "docs/setup.md",
        "src/algoarcade/games/firered/symbols.py",
        "tests/metadata/x.json",
        "docs/statement.md",
    ],
)
def test_allows_ordinary_files(name: str) -> None:
    assert guard_files.problem(name) is None


def test_rejects_large_files(tmp_path) -> None:
    big = tmp_path / "blob.bin"
    big.write_bytes(b"0" * (guard_files.MAX_BYTES + 1))
    assert guard_files.problem(str(big))


def test_main_reports_each_bad_file(capsys) -> None:
    assert guard_files.main(["a.gba", "README.md"]) == 1
    assert "a.gba" in capsys.readouterr().err
    assert guard_files.main(["README.md"]) == 0
