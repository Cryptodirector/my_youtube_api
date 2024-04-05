from fastapi import APIRouter
from app.main.service import MainService
from fastapi import Request
from app.main.schemas import AddVideoSchemas, UpdateVideoSchemas, AddCommentSchemas
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix='/api',
    tags=['Основной функционал']
)


@router.get('/main')
@cache(expire=60)
async def all_video():
    return await MainService.get_all_video()


@router.post('/add_video')
async def add_videos(
        video: AddVideoSchemas,
        request: Request
):
    return await MainService.add_video(request=request, video=video)


@router.get('/look_my_video')
async def get_my_video(request: Request):
    return await MainService.look_my_video(request)


@router.delete('/delete_video')
async def delete(id: int):
    return await MainService.delete_my_video(id)


@router.patch('/update_video')
async def update(video: UpdateVideoSchemas):
    return await MainService.change_video(video)


@router.get('/search')
async def search(title: str):
    return await MainService.search_video(title)


@router.post('/add_comment')
async def comment_add(
        request: Request,
        comment: AddCommentSchemas,
        id: int
):
    return await MainService.add_comment(request, comment, id)


@router.patch('/change_comment')
async def comment_change(
        request: Request,
        comment: AddCommentSchemas,
        id: int
):
    return await MainService.change_comment(request, id, comment)


@router.delete('/delete_comment')
async def comment_delete(
        request: Request,
        id: int
):
    return await MainService.delete_comment(request, id)