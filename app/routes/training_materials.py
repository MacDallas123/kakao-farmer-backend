from fastapi import APIRouter, Depends, HTTPException
from app.models import TrainingMaterial
from app.schemas import TrainingMaterialCreate, TrainingMaterialResponse
from app.auth import get_current_user, is_admin

router = APIRouter()

@router.post("/training_materials/", response_model=TrainingMaterialResponse, dependencies=[Depends(is_admin)])
async def create_training_material(material: TrainingMaterialCreate):
    new_material = await TrainingMaterial.create(**material.dict())
    return new_material

@router.delete("/training_materials/{material_id}", dependencies=[Depends(is_admin)])
async def delete_training_material(material_id: int):
    material = await TrainingMaterial.filter(id=material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    await material.delete()
    return {"msg": "Training material deleted successfully"}

@router.get("/training_materials/", response_model=list[TrainingMaterialResponse])
async def get_training_materials():
    materials = await TrainingMaterial.all()
    return materials