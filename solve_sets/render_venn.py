# This file render properly venn diagrams powered by matplotlib_venn
import io
import base64
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn3

# @param {sets_number}: number of sets
# @returns Bool
def is_renderable(sets_number: int):
    return sets_number == 2 or sets_number == 3


# @param {v}: Venn Diagram
# @returns: String base64, format png of Venn Diagram
def render_venn(v):
    plt.get(v)
    data = io.BytesIO()
    plt.savefig(data, format="png")
    b64 = base64.b64encode(data.getvalue()).decode()
    data.flush()
    data.seek(0)
    plt.clf()
    plt.close()
    return b63


# @param { data }: list of ID
# @param { v }: matiplot venn graph
def set_text_venn(data: list, v):
    for item in data:
        try:
            v.get_label_by_id(item["id"]).set_text(item["text_value"])
        except:
            pass
    return v


# @param {A}: set
# @param {B}: set
# @param {a_label}: Set A name
# @param {b_label}: Set B name
# @returns: matiplot Venn diagram
def graph_venn2(A: set, B: set, a_label: str, b_label: str):
    v = venn2(([A, B]), (a_label, b_label), alpha=0.4)
    venn_data = [
        {"id": "10", "text_value": "\n".join(sorted(A - B))},
        {"id": "01", "text_value": "\n".join(sorted(B - A))},
        {"id": "11", "text_value": "\n".join(sorted(A & B))},
    ]
    v = set_text_venn(venn_data, v)
    plt.title(f"Diagrama entre {a_label} y {b_label}")
    return v


# @param {A}: set
# @param {B}: set
# @param {C}: set
# @param {a_label}: Set A name
# @param {b_label}: Set B name
# @param {c_label}: Set C Name
# @returns: matiplot Venn diagram
def graph_venn3(A: set, B: set, C: set, a_label: str, b_label: str, c_label: str):
    v = venn3(((A, B, C)), (a_label, b_label, c_label), alpha=0.4)
    venn_data = [
        {"id": "100", "text_value": "\n".join(sorted(A - B - C))},
        {"id": "110", "text_value": "\n".join(sorted(A & B - C))},
        {"id": "010", "text_value": "\n".join(sorted(B - C - A))},
        {"id": "101", "text_value": "\n".join(sorted(A & C - B))},
        {"id": "111", "text_value": "\n".join(sorted(A & B & C))},
        {"id": "011", "text_value": "\n".join(sorted(B & C - A))},
        {"id": "001", "text_value": "\n".join(sorted(C - B - A))},
    ]
    v = set_text_venn(venn_data, v)
    plt.title(f"Diagrama de venn entre {a_label}, {b_label} y {c_label}")
    return v


# @param {sets}: group of sets
# @returns a Graphical Venn
def graph_venn(sets):
    if is_renderable(len(sets)):
        if len(sets) == 2:
            v = graph_venn2(
                sets[0]["setValue"],
                sets[1]["setValue"],
                sets[0]["setName"],
                sets[1]["setName"],
            )
            return render_venn(v)
        else:
            v = graph_venn3(
                sets[0]["setValue"],
                sets[1]["setValue"],
                sets[2]["setValue"],
                sets[0]["setName"],
                sets[1]["setName"],
                sets[2]["setName"],
            )
            return render_venn(v)


if __name__ == "__main__":
    pass
