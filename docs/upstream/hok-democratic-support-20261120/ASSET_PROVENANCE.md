# Democratic support and intelligence artwork provenance

This record identifies the six unchanged presentation payloads selected by the HOK update. Their exact donor bytes are preserved under this capsule's `runtime/` and recorded in [source-manifest.json](source-manifest.json). The compatibility generator owns delivery to the corresponding runtime paths and their GFX consumers. No new drawing, image generation, recolouring, resampling or binary conversion was performed.

## Authorship and retained notices

The eye focus, shine overlay and intelligence-spirit portrait originate in the installed Hearts of Iron IV game. Their rights remain with **Paradox Interactive and the relevant rights holders**; no individual artist was identified by the donor record. The donor's [asset credits](documents/docs/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_ASSET_CREDITS.md) preserve its 2026-11-18 review of the Paradox User Agreement and its scoped noncommercial HOI4-mod basis. This import does not claim a new legal review, transfer of rights or independently licensed asset pack. The intelligence focus retains its La Résistance gate in the integration's scoped behaviour.

The three decision images reuse the existing civic compositions: underlying art by **Globvs / Ultimate HOI4 GFX contributors**, with existing composition and blue-background work by **kpopmodder**. The fixed pack revision is `3626dc83c8573d6603fa497138090b04b64a15ba`; the [unchanged contributor notice](documents/docs/assets/korean-civic-decision-icons/sources/CREDITS.txt) is 1,029 bytes with SHA-256 `CF220DC66463D75163F7690AD77B02B662D0C05CA5D53DC62D33ED504512A7F5`. The [earlier civic credits](documents/docs/HOK_KOREAN_CHAEBOL_CIVIL_SOCIETY_ASSET_CREDITS.md) and [component manifest](documents/docs/data/HOK_KOREAN_CIVIC_DECISION_ICON_MANIFEST.json) retain the composition provenance. No MIT, Creative Commons or other new licence is asserted.

The HOK continuation contribution is selection, exact internal copies, dedicated sprite names and path integration. The compatibility contribution is source preservation, RT56 integration and semantic English text. Neither claims authorship of the inherited artwork.

## Current source comparison

On 2026-11-20 each capsule payload was compared byte-for-byte with both the clean donor checkout and its designated installed-game or existing donor-civic original. All six comparisons matched. The source root for game assets is `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV`; the civic source root is the read-only donor `C:\hoi\hearts_of_korea`.

All six are uncompressed BGRA32 DDS files with one image frame. Values below were read from the unchanged DDS headers and pixel alpha channels. Source paths are relative to the corresponding root; delivered paths are relative to the compatibility root and follow the preserved [asset manifest](documents/docs/data/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_ASSET_MANIFEST.json).

| Delivered payload | Designated source | Dimensions | Alpha min–max | Bytes | SHA-256 |
|---|---|---:|---:|---:|---|
| `gfx/interface/goals/HOK_KOR/democratic_intelligence/secret_intelligence_service.dds` | Game `gfx/interface/goals/focus_generic_secret_service_agency.dds` | 100×88 | 0–255 | 35,328 | `22EEEC2EDED697BDDA8396B98AE946590B1709E2C5963812EB309D50EB295C7A` |
| `gfx/interface/goals/HOK_KOR/democratic_intelligence/shine_overlay.dds` | Game `gfx/interface/goals/shine_overlay.dds` | 87×88 | 253–255 | 30,752 | `BB416649358C73D34AACD46BAD61BC44211FAC8111627B56E25F385AD98F4448` |
| `gfx/interface/ideas/HOK_KOR/democratic_intelligence/secret_intelligence_service.dds` | Game `gfx/interface/ideas/generic_spy_intel.dds` | 58×63 | 0–255 | 14,744 | `7309968400A39EB3DB4AB309A34ACB393D0C66A728DBFF2F2793B7667FDE3249` |
| `gfx/interface/decisions/HOK_KOR/democratic_support/category.dds` | Donor `gfx/interface/decisions/HOK_KOR/civic/category.dds` | 51×40 | 0–255 | 8,288 | `BAFBBC102E4DA51AB05CA9B15910DEA930DC1461994BEF4EB373A5A6381CD937` |
| `gfx/interface/decisions/HOK_KOR/democratic_support/support_democracy_in_japan.dds` | Donor `gfx/interface/decisions/HOK_KOR/civic/influence_blue.dds` | 32×32 | 0–255 | 4,224 | `C305D3C1C4A747E060F8ACA551678CEBF6A5986FD91467FB34161B0FCB7F19AB` |
| `gfx/interface/decisions/HOK_KOR/democratic_support/support_democracy_in_china.dds` | Donor `gfx/interface/decisions/HOK_KOR/civic/influence_blue.dds` | 32×32 | 0–255 | 4,224 | `C305D3C1C4A747E060F8ACA551678CEBF6A5986FD91467FB34161B0FCB7F19AB` |

The two support decisions intentionally share the existing blue scales motif. The category intentionally retains its existing grey civic composition. The information-service focus and spirit retain the selected original colours and dimensions, including the spirit's 58×63 size. The preserved dedicated [GFX registry](runtime/interface/HOK_KOR_democratic_support_intelligence.gfx) and [shine registry](runtime/interface/HOK_KOR_democratic_support_intelligence_shine.gfx) reference these internal copies without redefining the original game sprites.

The external report is `C:\hoi\test\hok-rt56-democratic-architecture-20261120-01\capsule\english-and-assets-report.json`. This verification establishes byte equality, dimensions, format and alpha metadata. It does not establish actual effective load precedence, focus/decision/idea rendering, shine behaviour or UI readability in RT56; those remain runtime verification items for the integration. No new image previews were generated by this subtask.
