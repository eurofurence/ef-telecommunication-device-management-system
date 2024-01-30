/**
 * Definition of a Vuetify DataTable header.
 */
export type TableHeader = {
    key: string;        /** Key of the property to display. */
    title: string;      /** Title of column */
    align?: string;     /** Alignment of column */
    sortable?: boolean; /** Whether column is sortable */
}
