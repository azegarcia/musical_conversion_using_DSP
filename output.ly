
    \version "2.22.2"
    \header {
        title = "Yung_Kai_-_Blue"
        subtitle = "Instrument: Piano"
        composer = ""
        arranger = ""
        opus = "Op. 1"
        }
        \score {
            \new Staff {
                \clef treble
                \time 4/4
                \tempo 4 = 80
                a,,4 ais,,4 e'4 b,,4 b'4 gis,,4 e,4 cis,4 cis,4 a,4 e,4 c,4 \break
c,4 b4 b,4 e'4 b,4 b4 dis,,4 dis,4 e,4 e4 a,4 b,,4 \break
a4 fis4 f,4 a,,4 e''4 e4 e,4 b,,4 fis,4 a,,4 e,4 f4 \break
ais,,4 fis,4 ais,,4 c,4 d,4 e4 e'4 cis4 gis'4 g,,4 e4 cis4 \break
e4 fis,4 e4 fis,4 a4 dis,,4 c,4 cis,4 dis'4 b4 g,4 f,4 \break
b4 fis4 a,,4 g,4 a4 d,,4 dis''4 a,4 gis,4 cis4 e'4 fis'4 \break
b'4 e4 b'4 e''4 a'4 gis''4 dis,4 dis,4 gis4 d4 d,4 dis'4 \break
b,4 g,,4 cis'4 b'4 b'4 e'4 b4 e''4 gis,,4 fis'4 a4 cis'4 \break
dis''4 a4 \break
            }
            \layout {
                \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/4)
            }
        }
    