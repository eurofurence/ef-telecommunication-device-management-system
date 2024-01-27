/**
 * Metadata required to construct a generic server side table with dynamic
 * content.
 */
export type ServerTableMetadata = {
    headers: {
        key: string;
        title: string;
        align?: string;
        sortable?: boolean;
    }[];
    fetchFunction: Function;
    search: string;
    loading: boolean;
    itemsPerPage: number;
    serverItems?: any[];
    totalItems?: number;
}