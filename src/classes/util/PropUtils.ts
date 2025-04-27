/* Eurofurence Telecommunication Device Management System (EF-TDMS)
 * Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>
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