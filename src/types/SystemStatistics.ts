/**
 * Definition of a SystemStatistics API response.
 */
export type SystemStatistics = {
    users: {
        total: number,
        with_bindings: number,
        without_bindings: number,
    },
    templates: object,
    items: {
        templates: number,
        total: number,
        bound: number,
        private: number,
    },
}
