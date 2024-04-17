import {TableHeader} from "@/types/TableHeader";
import {ExpandedRowProp} from "@/types/ExpandedRowProps";

/**
 * Metadata required to construct a generic server side table with dynamic
 * content.
 */
export type ServerTableMetadata = {
    headers: TableHeader[];                 /** Headers of the table. */
    fetchFunction: Function;                /** Function to fetch a page of data. */
    expandedRowProps?: ExpandedRowProp[];   /** Properties to display in an expanded row. */
    search?: string;                        /** Search string to filter by. */
    itemsPerPage?: number;                  /** Number of items per page. */
    preventCreate?: boolean;                /** Prevent creating new items. */
    preventEdit?: boolean;                  /** Prevent editing items. */
    preventDelete?: boolean;                /** Prevent deleting items. */
}