public enum AWB {

    /**
     * Turns off white balance calculation.
     */
    OFF,

    /**
     * Automatic mode (default)
     */
    AUTO,

    /**
     * Sunny mode.
     */
    SUN,

    /**
     * Cloudy mode.
     */
    CLOUD,

    /**
     * Shaded mode.
     */
    SHADE,

    /**
     * Tungsten lighting mode.
     */
    TUNGSTEN,

    /**
     * Fluorescent lighting mode.
     */
    FLUORESCENT,

    /**
     * Incandescent lighting mode.
     */
    INCANDESCENT,

    /**
     * Flash mode.
     */
    FLASH,

    /**
     * Horizon mode.
     */
    HORIZON;

    /**
     * Returns enum in lowercase.
     */
    public String toString() {
        String id = name();
        return id.toLowerCase();
    }
}