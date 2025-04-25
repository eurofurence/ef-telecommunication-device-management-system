/* Eurofurence Telecommunication Device Management System (EF-TDMS)
 * Copyright (C) 2024 Niels Gandraß <niels@gandrass.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

import type {TableHeader} from "@/types/TableHeader";
import type {ExpandedRowProp} from "@/types/ExpandedRowProps";

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
    alwaysShowMapButton?: boolean;          /** Always show the map button. */
}