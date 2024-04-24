export class IconUtils {

    /**
     * Generates an mdi-map-marker icon with the specified color
     *
     * @param color The color of the icon in hexadecimal format (e.g. #000000)
     */
    public static MapMarker(color = '#000000') {
        return 'data:image/svg+xml;base64,' + btoa(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">' +
                '<path style="fill:' + color + ';" d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z"/>' +
            '</svg>'
        );
    }

}