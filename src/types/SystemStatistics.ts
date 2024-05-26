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
        total: number,
        bound: number,
        unbound: number,
    },
}
