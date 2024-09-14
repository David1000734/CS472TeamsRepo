package nl.tudelft.jpacman.level;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;

import nl.tudelft.jpacman.sprite.Sprite;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

public class PelletValueTest {

    // Mimics input to test to see what would happen
    // Idea sourced from BoardTest.java
    @ParameterizedTest
    @CsvSource({
        "1",
        "2",
        "3",
        "25",
        "367",
        "-5",
        "01",
        "20000",
        "-453"
    })
    void testPelletValue(int x) {

        // Makes a pellet object
        Pellet pelletPoint = new Pellet(x, mock(Sprite.class));

        // Checks that its value is the same as inputted
        assertThat(pelletPoint.getValue()).isEqualTo(x);
    }
}
