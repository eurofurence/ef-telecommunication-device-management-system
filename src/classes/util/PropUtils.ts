export class PropUtils {

    /**
     * Gets a property from an object by a dot-delimited string path.
     *
     * @param obj Object to get the property from.
     * @param path Dot-delimited string path to the property.
     */
    public static getPropByStringPath(obj: any, path: string) {
        return path.split('.').reduce((acc, part) => acc && acc[part], obj)
    }

}