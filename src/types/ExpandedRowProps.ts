/**
 * A single property to be displayed inside an expanded row of an ItemTable.
 */
export type ExpandedRowProp = {
    key: string;            /** Key of the property to display. */
    title: string;          /** Title of the property to be display alongside its value. */
    hideMissing?: boolean;  /** If true, the property title will be hidden if its value is empty. */
};