export class PropUtils {

    /**
     * Gets a property from an object by a dot-delimited string path.
     *
     * @param obj Object to get the property from.
     * @param path Dot-delimited string path to the property.
     * @returns The property value, or undefined if the path is invalid.
     */
    public static getPropByStringPath(obj: any, path: string) {
        try {
            return path.split('.').reduce((acc, part) => acc && acc[part], obj)
        } catch (e) {
            return undefined;
        }
    }

}