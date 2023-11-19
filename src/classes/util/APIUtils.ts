interface VuetifyTableSortByEntry {
    key: string;
    order: string;
}

export class APIUtils {

    /**
     * Converts a Vuetify table ordering to a DRF query parameter.
     *
     * @param sortBy Vuetify table ordering.
     *
     * @returns DRF query parameter.
     */
    public static vuetifyTableOrderingToQueryParameter(sortBy: VuetifyTableSortByEntry[]): string {
        let ordering = '';

        sortBy.forEach((item: any) => {
            ordering += (item.order === 'asc') ? item.key : '-' + item.key;
        });

        return ordering;
    }

}