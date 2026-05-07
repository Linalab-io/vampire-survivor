import pyxel


def _scale_volume_pattern(pattern, volume):
    def scale_digit(char):
        if char.isdigit():
            return str(max(0, min(7, round(int(char) * volume))))
        return char

    return "".join(scale_digit(char) for char in pattern)


def create_sounds(bgm_volume=4, sfx_volume=0.8):
    pyxel.sound(0).set("g4 c4", "pp", _scale_volume_pattern("77", sfx_volume), "n", 2)  # type: ignore[attr-defined]
    pyxel.sound(1).set("c3 e3", "ss", _scale_volume_pattern("77", sfx_volume), "n", 2)  # type: ignore[attr-defined]
    pyxel.sound(2).set("c3 e3 g3", "ppp", _scale_volume_pattern("777", sfx_volume), "nnn", 3)  # type: ignore[attr-defined]

    pyxel.sound(3).set(  # type: ignore[attr-defined]
        notes="c3 e3 g3 c4 e4 c4 g3 e3 c3 e3 g3 c4 e4 c4 g3 e3",
        tones="t",
        volumes=str(min(7, bgm_volume + 1)),
        effects="n",
        speed=8,
    )
    pyxel.sound(4).set(  # type: ignore[attr-defined]
        notes="c2 c2 g2 g2 a2 a2 e2 e2 f2 f2 c2 c2 g2 g2 c2 c2",
        tones="s",
        volumes=str(bgm_volume),
        effects="n",
        speed=8,
    )
    pyxel.music(0).set([3, 4], [], [], [])  # type: ignore[attr-defined]

    pyxel.sound(5).set(notes="e4 d4 c4", tones="n", volumes=_scale_volume_pattern("6 4 2", sfx_volume), effects="s", speed=3)  # type: ignore[attr-defined]
    pyxel.sound(6).set(notes="c4 e4 g4 a4", tones="t", volumes=_scale_volume_pattern("7 6 5 7", sfx_volume), effects="n", speed=5)  # type: ignore[attr-defined]
    pyxel.sound(7).set(notes="c2 c2 c2 c2", tones="n", volumes=_scale_volume_pattern("7 7 6 5", sfx_volume), effects="s", speed=4)  # type: ignore[attr-defined]
    pyxel.sound(8).set(notes="e3 g3 b3 e4", tones="t", volumes=_scale_volume_pattern("4 5 6 4", sfx_volume), effects="f", speed=6)  # type: ignore[attr-defined]
    pyxel.sound(9).set(notes="g4", tones="s", volumes=_scale_volume_pattern("4", sfx_volume), effects="n", speed=2)  # type: ignore[attr-defined]
